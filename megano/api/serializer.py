from rest_framework import serializers
from products.models import ProductFull, Image, Tag, Category, Review, Specifications, CategoryImage
from profiles.models import Profile, Avatar
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






class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = 'scr', 'alt'


class ProfilesSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer()

    class Meta:
        model = Profile
        fields = 'fullName', 'email', 'phone', 'avatar'




