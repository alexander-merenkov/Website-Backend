import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest, HttpResponseRedirect
from random import randrange
import json
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.db.models import Q
from api.serializer import (
	ProductFullSerializer,
	ReviewSerializer,
	TagSerializer,
	ProfilesSerializer,
	ProductSaleSerializer,
	CategorySerializer, OrderSerializer, OrdersSerializer,
)
from products.models import ProductFull, Review, Tag, Category
from shop.models import Basket, BasketItem, Order, Orders, Discount, Payment
from math import ceil
from django.db.models import Count
from rest_framework.decorators import api_view
from django.urls import reverse
from django.db import IntegrityError
from profiles.models import Profile, Avatar
from django.db import transaction
from django.contrib.sessions.backends.db import SessionStore


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
	category = request.GET.get('category')

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
	if category:
		products = products.filter(category=category)

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

		# Authenticated
		if request.user.is_authenticated:
			basket = Basket.objects.get(user=request.user)
			basket_items = BasketItem.objects.filter(basket=basket)
			data = []
			for basket_item in basket_items:
				serialized = ProductFullSerializer(basket_item.product)
				new_data = serialized.data
				new_data['count'] = basket_item.count
				data.append(new_data)

			return JsonResponse(data, safe=False)


		# Anonymous
		elif request.user.is_anonymous:
			session_key = request.COOKIES.get('sessionid')
			if session_key:
				session = SessionStore(session_key=session_key)
				basket_id = session.get('basket_id')

			if basket_id:
				basket = Basket.objects.filter(id=basket_id).first()

				if basket is None:
					data = []
				else:
					basket_items = BasketItem.objects.filter(basket=basket)
					data = []
					for basket_item in basket_items:
						serialized = ProductFullSerializer(basket_item.product)
						new_data = serialized.data
						new_data['count'] = basket_item.count
						data.append(new_data)
			else:
				data = []

			return JsonResponse(data, safe=False)



	elif (request.method == "POST"):
		body = json.loads(request.body)
		product_id = body['id']
		count = body['count']
		user = request.user

		# Anonymous
		if user.is_anonymous:
			session_key = request.COOKIES.get('sessionid')

			if session_key:
				session = SessionStore(session_key=session_key)
			else:
				session = SessionStore()
			if 'basket_id' not in session:
				basket = Basket.objects.create()
				session['basket_id'] = basket.id
				session.save()
			else:
				basket_id = session['basket_id']
				basket = Basket.objects.get(id=basket_id)


			product = ProductFull.objects.get(id=product_id)
			basket_item, item_created = BasketItem.objects.get_or_create(
				basket=basket,
				product=product,
			)
			if item_created:
				basket_item.count = count
			else:
				if count:
					basket_item.count += int(count)

			basket_item.save()

			serialized = ProductFullSerializer(product)
			data = serialized.data
			response = JsonResponse(data, safe=False)
			response.set_cookie('sessionid', session.session_key)

			return response


		# Authenticated
		if user.is_authenticated:
			basket, basket_created = Basket.objects.get_or_create(user=user)
			product = ProductFull.objects.get(id=product_id)
			basket_item, item_created = BasketItem.objects.get_or_create(
				basket=basket,
				product=product,
			)
			if item_created:
				basket_item.count = count
			else:
				if count:
					basket_item.count += int(count)

			basket_item.save()

			serialized = ProductFullSerializer(product)
			data = serialized.data

			return JsonResponse(data, safe=False)

	elif (request.method == "DELETE"):
		body = json.loads(request.body)
		product_id = body['id']
		count = body['count']
		user = request.user

		# Authenticated
		if user.is_authenticated:
			basket = Basket.objects.get(user=user)
			product = ProductFull.objects.get(id=product_id)

			try:
				basket_item = BasketItem.objects.get(
					basket=basket,
					product=product,
				)
			except ObjectDoesNotExist:
				return HttpResponse(status=500)

			if basket_item.count == 1:
				basket_item.delete()

			else:
				basket_item.count -= count
				if basket_item.count < 0:
					basket_item.delete()
				basket_item.save()
				if basket_item.count == 0:
					basket_item.delete()


			serialized = ProductFullSerializer(product)
			data = serialized.data

			return JsonResponse(data, safe=False)

		# Anonymous
		elif user.is_anonymous:
			session_key = request.COOKIES.get('sessionid')
			if session_key:
				session = SessionStore(session_key=session_key)
				basket_id = session.get('basket_id')

			if basket_id:
				basket = Basket.objects.filter(id=basket_id).first()
				product = ProductFull.objects.get(id=product_id)

				try:
					basket_item = BasketItem.objects.get(
						basket=basket,
						product=product,
					)
				except ObjectDoesNotExist:
					return HttpResponse(status=500)

				if basket_item.count == 1:
					basket_item.delete()

				else:
					basket_item.count -= count
					if basket_item.count < 0:
						basket_item.delete()
					basket_item.save()
					if basket_item.count == 0:
						basket_item.delete()

				serialized = ProductFullSerializer(product)
				data = serialized.data

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
	if request.method == "POST":
		body = json.loads(request.body)
		username = body['username']
		password = body['password']

		if not username or not password:
			return HttpResponse(status=500)

		try:
			User.objects.create_user(username=username, password=password)
			user = authenticate(request, username=username, password=password)
			login(request, user)
			return HttpResponse(status=200)

		except IntegrityError as ecx:
			return HttpResponse('User is already exist', status=500)


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


def profile(request: HttpRequest):
	if(request.method == 'GET'):
		profile = Profile.objects.get(user=request.user)
		serialized = ProfilesSerializer(profile)
		data = serialized.data
		return JsonResponse(data)

	elif(request.method == 'POST'):
		data = json.loads(request.body)
		fullName = data['fullName']
		phone = data['phone']
		email = data['email']

		profile, created = Profile.objects.get_or_create(user=request.user)
		profile.user = request.user
		profile.fullName = fullName
		profile.phone = phone
		profile.email = email
		profile.save()

		return JsonResponse(data)

	return HttpResponse(status=500)


def profilePassword(request):
	data = json.loads(request.body)
	currentPassword = data['currentPassword']
	newPassword = data['newPassword']

	user = authenticate(username=request.user.username, password=currentPassword)

	if user is None:
		return HttpResponse(status=500)

	user.set_password(newPassword)
	user.save()
	update_session_auth_hash(request, user)

	return HttpResponse(status=200)


def orders(request):
	if(request.method == 'GET'):
		orders = Orders.objects.all().filter(user=request.user)
		serialized = OrdersSerializer(orders, many=True)
		data = serialized.data[0]
		data = sorted(data, key=lambda x: x['createdAt'], reverse=True)
		return JsonResponse(data, safe=False)

	elif(request.method == 'POST'):
		if request.user.is_authenticated:
			try:
				order = Order.objects.get(status='created', user=request.user)
			except ObjectDoesNotExist:
				profile, created_profile = Profile.objects.get_or_create(user=request.user)

				if created_profile:

					profile.fullName = request.user.username
					profile.save()

				order = Order.objects.create(
					user=request.user,
					fullName=profile.fullName,
					email=profile.email,
					phone=profile.phone,
					status='created',
				)

			data = {
				"orderId": order.pk,
			}
			return JsonResponse(data)

		return HttpResponse('user is not is_authenticated', status=500)


@transaction.atomic
def order(request, id):

	basket = Basket.objects.get(user=request.user)
	basket_items = BasketItem.objects.filter(basket=basket)

	order = Order.objects.get(pk=id)

	for basket_item in basket_items:
		basket_item.product.count = basket_item.count
		basket_item.product.save()
		order.products.add(basket_item.product)

	serialized = OrderSerializer(order)
	data = serialized.data

	if(request.method == 'GET'):
		return JsonResponse(data)

	elif(request.method == 'POST'):
		body = json.loads(request.body)
		order.createdAt = timezone.now()
		order.fullName = body['fullName']
		order.email = body['email']
		order.phone = body['phone']
		order.deliveryType = body['deliveryType']
		order.paymentType = body['paymentType']
		order.city = body['city']
		order.address = body['address']

		total_cost = 0
		discount = Discount.get_discount()

		for product in order.products.all():
			total_cost += product.count * product.price

		if order.deliveryType == 'express':
			total_cost += discount.express

		elif order.deliveryType == 'ordinary' and total_cost < discount.limit:
			total_cost += discount.regular

		order.totalCost = total_cost
		order.status = 'payment required'
		order.save()

		orders, orders_created = Orders.objects.get_or_create(user=request.user)

		try:
			_ = orders.orders.get(id=order.id)
		except ObjectDoesNotExist:
			orders.orders.add(order)

		basket_items.delete()


		data = {"orderId": order.pk}

		return JsonResponse(data)

	return HttpResponse(status=500)


def payment(request, id):
	data = json.loads(request.body)
	name = data['name']
	number = data['number']
	year = data['year']
	month = data['month']
	code = data['code']

	print(data)
	error = None

	try:
		number = int(number)
	except ValueError:
		error = 'invalid card number'

	order = Order.objects.get(pk=id)
	if order.status == 'payed':
		return HttpResponse('Order payed', status=500)

	payment, _ = Payment.objects.get_or_create(order=order)
	payment.name=name
	payment.number=number
	payment.year=year
	payment.month=month
	payment.code=code
	payment.save()

	if error:
		order.status = error
		order.save()

	elif number % 2 != 0 or number % 10 == 0:
		order.status = 'invalid card number'
		order.save()

	else:
		order.status = 'payed'
		order.save()

	print(order.status)

	return HttpResponse(status=200)


def avatar(request):
	if request.method == "POST":
		myfile = request.FILES['avatar']
		fs = FileSystemStorage()
		if myfile.size < 2097152:
			path = 'users/user_{pk}/avatar/{filename}'.format(
				pk=request.user.pk,
				filename=myfile.name,
			)
			fs.save(path, myfile)

			profile= Profile.objects.get(user=request.user)

			if profile.avatar:
				avatar = profile.avatar
				fs.delete(avatar.src.path)
				avatar.src = path
				avatar.alt = f"Avatar of {profile.user}"
			else:
				avatar = Avatar.objects.create(src=path, alt=f"Avatar of {profile.user}")

			avatar.save()
			profile.avatar = avatar
			profile.save()

		else:
			print('File Size is too big')
			return HttpResponse('File is more than 2mb', status=200)
		return HttpResponse(status=200)