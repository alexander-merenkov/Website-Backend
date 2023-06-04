from rest_framework import serializers
from products.models import ProductFull, Image, Tag, Category, Review


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


class ProductFullSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    category = CategorySerializer()

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

