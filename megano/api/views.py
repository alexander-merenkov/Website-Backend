from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponseRedirect
from random import randrange
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.db.models import Q
from api.serializer import (
	ProductFullSerializer,
	ReviewSerializer,
	TagSerializer,
	ProfilesSerializer,
	ProductSaleSerializer,
	CategorySerializer
)
from products.models import ProductFull, Review, Tag, Category
from math import ceil
from django.db.models import Count
from rest_framework.decorators import api_view
from django.urls import reverse

from profiles.models import Profile

User = get_user_model()


def banners(request):
	random_objects = ProductFull.objects.order_by('?')[:2]
	serializer = ProductFullSerializer(random_objects, many=True)
	data = serializer.data
	return JsonResponse(data, safe=False)


def categories(request):
	category_list = Category.objects.all()
	serialized = CategorySerializer(category_list, many=True)
	data = serialized.data

	return JsonResponse(data, safe=False)


def catalog(request):

	filter_title = request.GET.get('filter[name]', '')
	filter_min_price = request.GET.get('filter[minPrice]', 0)
	filter_max_price = request.GET.get('filter[maxPrice]', 50000)
	filter_free_delivery = request.GET.get('filter[freeDelivery]')
	filter_available = request.GET.get('filter[available]')
	current_page = int(request.GET.get('currentPage', 1))
	sort_field = request.GET.get('sort', 'price')
	sort_type = request.GET.get('sortType', 'inc')
	limit = int(request.GET.get('limit', 20))
	tags = request.GET.getlist('tags[]')

	if filter_free_delivery == 'true':
		filter_free_delivery = True
	elif filter_free_delivery == 'false':
		filter_free_delivery = None

	if filter_available == 'true':
		filter_available = True
	elif filter_available == 'false':
		filter_available = None

	products = ProductFull.objects.filter(
		Q(title__icontains=filter_title) | Q(description__icontains=filter_title),
		price__gte=filter_min_price,
		price__lte=filter_max_price,
	)

	if filter_available:
		products = products.filter(available=filter_available)

	if filter_free_delivery:
		products = products.filter(freeDelivery=filter_free_delivery)

	if tags:
		for tag in tags:
			products = products.filter(tags__pk=tag)

	if sort_field == 'reviews':
		products = products.annotate(num_reviews=Count('reviews'))
		sort_field = 'num_reviews'

	if sort_type == 'inc':
		products = products.order_by(sort_field)
	elif sort_type == 'dec':
		products = products.order_by(f'-{sort_field}')

	total_count = products.count()
	page_count = ceil(total_count / limit)

	start_index = (current_page - 1) * limit
	end_index = start_index + limit
	products = products[start_index:end_index]

	serializer = ProductFullSerializer(products, many=True)
	data = {
		'items': serializer.data,
		'currentPage': current_page,
		'lastPage': page_count,
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
	products = ProductFull.objects.exclude(salePrice__isnull=True)
	current_page = int(request.GET.get('currentPage', 1))
	limit = int(request.GET.get('limit', 20))

	total_count = products.count()
	page_count = ceil(total_count / limit)

	start_index = (current_page - 1) * limit
	end_index = start_index + limit
	products = products[start_index:end_index]

	serializer = ProductSaleSerializer(products, many=True)
	data = {
		'items': serializer.data,
		'currentPage': current_page,
		'lastPage': page_count,
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
	if request.method == 'POST':
		data = json.loads(request.body)
		serializer = ReviewSerializer(data=data)
		if serializer.is_valid():
			serializer.save(product_id=id)
			data = serializer.data
			return JsonResponse(data, safe=False)

		else:
			return JsonResponse({"error": "Incorrect Data"}, status=405)


@api_view(['GET'])
def profile(request: HttpRequest):
	if(request.method == 'GET'):
		if request.user.is_anonymous:
			redirect_url = reverse('frontend:sign-in')
			return HttpResponseRedirect(redirect_url)

		profile = Profile.objects.get(user=request.user)
		serialized = ProfilesSerializer(profile)
		data = serialized.data
		print(data)
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