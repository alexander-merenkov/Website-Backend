from rest_framework import serializers
from products.models import ProductFull, Image, Tag, Category, Review, Specifications
from profiles.models import Profile, Avatar


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = 'src', 'alt'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'id', 'name'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id', 'name'


class SpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specifications
        fields = 'name', 'value'


class ProductFullSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    category = CategorySerializer()
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





class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = 'scr', 'alt'


class ProfilesSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer()

    class Meta:
        model = Profile
        fields = 'fullName', 'email', 'phone', 'avatar'




