from rest_framework import serializers
from rest_framework.serializers import ListSerializer

from products.models import ProductFull, Image, Tag, Category, Review, Specifications, CategoryImage
from profiles.models import Profile, Avatar
from shop.models import Basket, BasketItem, Order, Orders
from django.conf import settings

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = 'src', 'alt'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'id', 'name'


class SpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specifications
        fields = 'name', 'value'


class ProductFullSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    specifications = SpecificationsSerializer(many=True)

    class Meta:
        model = ProductFull
        fields = (
            'id',
            'category',
            'price',
            'count',
            'date',
            'title',
            'description',
            'fullDescription',
            'freeDelivery',
            'images',
            'tags',
            'reviews',
            'specifications',
            'rating',
        )


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            'author',
            'email',
            'text',
            'rate',
            'date',
            'product',
        )


class ProductSaleSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    dateFrom = serializers.DateField(format='%m-%d')
    dateTo = serializers.DateField(format='%m-%d')

    class Meta:
        model = ProductFull
        fields = ['id', 'price', 'salePrice', 'dateFrom', 'dateTo', 'title', 'images']


class CategoryImageSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = CategoryImage
        fields = 'src', 'alt'

    def get_src(self, obj):
        file_name = obj.src.name
        file_url = settings.MEDIA_URL + file_name
        return file_url


class CategorySerializer(serializers.ModelSerializer):
    image = CategoryImageSerializer()

    class Meta:
        model = Category
        fields = 'id', 'title', 'image', 'subcategories'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['subcategories'] is None:
            representation['subcategories'] = ''
        return representation


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = 'src', 'alt'


class ProfilesSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer()

    class Meta:
        model = Profile
        fields = 'fullName', 'email', 'phone', 'avatar'


class OrderSerializer(serializers.ModelSerializer):
    products = ProductFullSerializer(many=True)
    createdAt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = Order
        fields = (
            'id',
            'createdAt',
            'fullName',
            'email',
            'phone',
            'deliveryType',
            'paymentType',
            'totalCost',
            'status',
            'city',
            'address',
            'products',
        )


class OrdersSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True)

    class Meta:
        model = Orders
        fields = 'orders',

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation['orders']
