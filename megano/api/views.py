from django.shortcuts import render
from django.http import JsonResponse
from random import randrange
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.db.models import Q
from api.serializer import ProductFullSerializer, ReviewSerializer, TagSerializer
from products.models import ProductFull, Review, Tag

User = get_user_model()



def banners(request):
	random_objects = ProductFull.objects.order_by('?')[:2]
	serializer = ProductFullSerializer(random_objects, many=True)
	data = serializer.data
	return JsonResponse(data, safe=False)


def categories(request):
	data = [
		 {
			 "id": 123,
			 "title": "video card",
			 "image": {
				"src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
				 "alt": "Image alt string"
			 },
			 "subcategories": [
				 {
					 "id": 123,
					 "title": "video card",
					 "image": {
							"src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
						 	"alt": "Image alt string"
					 }
				 }
			 ]
		 }
	 ]

	return JsonResponse(data, safe=False)


def catalog(request):

	filter_title = request.GET.get('filter[name]', '')
	filter_min_price = request.GET.get('filter[minPrice]', 0)
	filter_max_price = request.GET.get('filter[maxPrice]', 50000)
	filter_free_delivery = request.GET.get('filter[freeDelivery]', False)
	filter_available = request.GET.get('filter[available]', True)
	current_page = request.GET.get('currentPage', 1)
	sort_field = request.GET.get('sort', 'price')
	sort_type = request.GET.get('sortType', 'inc')
	limit = request.GET.get('limit', 20)

	if filter_free_delivery == 'true':
		filter_free_delivery = True
	elif filter_free_delivery == 'false':
		filter_free_delivery = False

	if filter_available == 'true':
		filter_available = True
	elif filter_available == 'false':
		filter_available = False

	products = ProductFull.objects.filter(
		Q(title__icontains=filter_title) | Q(description__icontains=filter_title),
		price__gte=filter_min_price,
		price__lte=filter_max_price,
		freeDelivery=filter_free_delivery,
		available=filter_available
	)

	if sort_type == 'inc':
		products = products.order_by(sort_field)
	elif sort_type == 'dec':
		products = products.order_by(f'-{sort_field}')

	total_count = products.count()

	start_index = (int(current_page) - 1) * int(limit)
	end_index = int(start_index) + int(limit)
	products = products[start_index:end_index]

	serializer = ProductFullSerializer(products, many=True)
	data = {
		'items': serializer.data,
		'totalCount': total_count
	}

	return JsonResponse(data)


def productsPopular(request):
	products = ProductFull.objects.order_by('-rating')
	serialized = ProductFullSerializer(products, many=True)
	data = serialized.data
	return JsonResponse(data, safe=False)


def productsLimited(request):
	products = ProductFull.objects.filter(limited_edition=True)[:16]
	serialized = ProductFullSerializer(products, many=True)
	data = serialized.data
	return JsonResponse(data, safe=False)


def sales(request):
	data = {
		'items': [
			{
				"id": 123,
				"price": 500.67,
				"salePrice": 200.67,
				"dateFrom": "05-08",
				"dateTo": "05-20",
				"title": "video card",
				"images": [
						{
							"src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
							"alt": "hello alt",
						}
				 ],
			}
		],
		'currentPage': randrange(1, 4),
		'lastPage': 3,
	}
	return JsonResponse(data)


def basket(request):
	if(request.method == "GET"):
		print('[GET] /api/basket/')
		data = [
			{
				"id": 123,
				"category": 55,
				"price": 500.67,
				"count": 12,
				"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
				"title": "video card",
				"description": "description of the product",
				"freeDelivery": True,
				"images": [
						{
							"src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
							"alt": "hello alt",
						}
				 ],
				 "tags": [
						{
							"id": 0,
							"name": "Hello world"
						}
				 ],
				"reviews": 5,
				"rating": 4.6
			},
			{
				"id": 124,
				"category": 55,
				"price": 201.675,
				"count": 5,
				"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
				"title": "video card",
				"description": "description of the product",
				"freeDelivery": True,
				"images": [
						{
							"src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
							"alt": "hello alt",
						}
				 ],
				 "tags": [
						{
							"id": 0,
							"name": "Hello world"
						}
				 ],
				"reviews": 5,
				"rating": 4.6
			}
		]
		return JsonResponse(data, safe=False)

	elif (request.method == "POST"):
		body = json.loads(request.body)
		id = body['id']
		count = body['count']
		print('[POST] /api/basket/   |   id: {id}, count: {count}'.format(id=id, count=count))
		data = [
			{
				"id": id,
				"category": 55,
				"price": 500.67,
				"count": 13,
				"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
				"title": "video card",
				"description": "description of the product",
				"freeDelivery": True,
				"images": [
						{
							"src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
							"alt": "hello alt",
						}
				 ],
				 "tags": [
						{
							"id": 0,
							"name": "Hello world"
						}
				 ],
				"reviews": 5,
				"rating": 4.6
			}
		]
		return JsonResponse(data, safe=False)

	elif (request.method == "DELETE"):
		body = json.loads(request.body)
		id = body['id']
		print('[DELETE] /api/basket/')
		data = [
			{
			"id": id,
			"category": 55,
			"price": 500.67,
			"count": 11,
			"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
			"title": "video card",
			"description": "description of the product",
			"freeDelivery": True,
			"images": [
					{
						"src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
						"alt": "hello alt",
					}
			 ],
			 "tags": [
					{
						"id": 0,
						"name": "Hello world"
					}
			 ],
			"reviews": 5,
			"rating": 4.6
			}
		]
		return JsonResponse(data, safe=False)

def orders(request):
	if (request.method == "POST"):
		data = [
			{
			"id": 123,
			"category": 55,
			"price": 500.67,
			"count": 12,
			"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
			"title": "video card",
			"description": "description of the product",
			"freeDelivery": True,
			"images": [
					{
						"src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
						"alt": "hello alt",
					}
			 ],
			 "tags": [
					{
						"id": 0,
						"name": "Hello world"
					}
			 ],
				"reviews": 5,
				"rating": 4.6
			}
		]
		return JsonResponse(data, safe=False)

def signIn(request):
	if request.method == "POST":
		body = json.loads(request.body)
		username = body['username']
		password = body['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponse(status=200)
		else:
			return HttpResponse(status=500)

def signUp(request):
	user = User.objects.create_user("mir232", "lennon@thebeatles.com", "pass232")
	user.save()
	return HttpResponse(status=200)

def signOut(request):
	logout(request)
	return HttpResponse(status=200)


def product(request, id):
	product_by_id = ProductFull.objects.get(pk=id)
	serializer = ProductFullSerializer(product_by_id)
	data = serializer.data

	reviews = Review.objects.filter(product=product_by_id)
	reviews_serializer = ReviewSerializer(reviews, many=True)
	data['reviews'] = reviews_serializer.data


	return JsonResponse(data)


def tags(request):
	tags = Tag.objects.all()
	serialized = TagSerializer(tags, many=True)
	data = serialized.data

	return JsonResponse(data, safe=False)


def productReviews(request, id):
	product_by_id = ProductFull.objects.get(pk=id)
	reviews = Review.objects.filter(product=product_by_id)
	reviews_serializer = ReviewSerializer(reviews, many=True)
	data = reviews_serializer.data

	if request.method == 'POST':
		data = json.loads(request.body)
		serializer = ReviewSerializer(data=data)
		if serializer.is_valid():
			serializer.save(product_id=id)
			data = serializer.data
			return JsonResponse(data, safe=False)

		else:
			return JsonResponse({"error": "Incorrect Data"}, status=405)


def profile(request):
	if(request.method == 'GET'):
		data = {
			"fullName": "Annoying Orange",
			"email": "no-reply@mail.ru",
			"phone": "88002000600",
			"avatar": {
				"src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
				"alt": "hello alt",
			}
		}
		return JsonResponse(data)

	elif(request.method == 'POST'):
		data = {
			"fullName": "Annoying Green",
			"email": "no-reply@mail.ru",
			"phone": "88002000600",
			"avatar": {
				"src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
				"alt": "hello alt",
			}
		}
		return JsonResponse(data)

	return HttpResponse(status=500)

def profilePassword(request):
	return HttpResponse(status=200)

def orders(request):
	if(request.method == 'GET'):
		data = [
			{
        "id": 123,
        "createdAt": "2023-05-05 12:12",
        "fullName": "Annoying Orange",
        "email": "no-reply@mail.ru",
        "phone": "88002000600",
        "deliveryType": "free",
        "paymentType": "online",
        "totalCost": 567.8,
        "status": "accepted",
        "city": "Moscow",
        "address": "red square 1",
        "products": [
          {
            "id": 123,
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
              {
                "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                "alt": "Image alt string"
              }
            ],
            "tags": [
              {
                "id": 12,
                "name": "Gaming"
              }
            ],
            "reviews": 5,
            "rating": 4.6
          }
        ]
      },
			{
        "id": 123,
        "createdAt": "2023-05-05 12:12",
        "fullName": "Annoying Orange",
        "email": "no-reply@mail.ru",
        "phone": "88002000600",
        "deliveryType": "free",
        "paymentType": "online",
        "totalCost": 567.8,
        "status": "accepted",
        "city": "Moscow",
        "address": "red square 1",
        "products": [
          {
            "id": 123,
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
              {
                "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                "alt": "Image alt string"
              }
            ],
            "tags": [
              {
                "id": 12,
                "name": "Gaming"
              }
            ],
            "reviews": 5,
            "rating": 4.6
          }
        ]
      }
		]
		return JsonResponse(data, safe=False)

	elif(request.method == 'POST'):
		data = {
			"orderId": 123,
		}
		return JsonResponse(data)

	return HttpResponse(status=500)

def order(request, id):
	if(request.method == 'GET'):
		data = {
			"id": 123,
			"createdAt": "2023-05-05 12:12",
			"fullName": "Annoying Orange",
			"email": "no-reply@mail.ru",
			"phone": "88002000600",
			"deliveryType": "free",
			"paymentType": "online",
			"totalCost": 567.8,
			"status": "accepted",
			"city": "Moscow",
			"address": "red square 1",
			"products": [
				{
					"id": 123,
					"category": 55,
					"price": 500.67,
					"count": 12,
					"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
					"title": "video card",
					"description": "description of the product",
					"freeDelivery": True,
					"images": [
						{
						"src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
						"alt": "Image alt string"
						}
					],
					"tags": [
						{
						"id": 12,
						"name": "Gaming"
						}
					],
					"reviews": 5,
					"rating": 4.6
				},
			]
		}
		return JsonResponse(data)

	elif(request.method == 'POST'):
		data = { "orderId": 123 }
		return JsonResponse(data)

	return HttpResponse(status=500)

def payment(request, id):
	print('qweqwewqeqwe', id)
	return HttpResponse(status=200)

def avatar(request):
	if request.method == "POST":
# 		print(request.FILES["avatar"])
		return HttpResponse(status=200)