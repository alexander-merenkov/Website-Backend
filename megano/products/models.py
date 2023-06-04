from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Image(models.Model):
    src = models.URLField()
    alt = models.CharField(max_length=100)

    def __str__(self):
        return self.alt


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductFull(models.Model):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    count = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    fullDescription = models.TextField(blank=True, null=True)
    freeDelivery = models.BooleanField()
    images = models.ManyToManyField(Image)
    tags = models.ManyToManyField(Tag)
    specifications = models.TextField(max_length=100, blank=True)
    rating = models.FloatField(null=True, blank=True)
    limited_edition = models.BooleanField(default=False)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    author = models.CharField(max_length=100, default='Unknown')
    email = models.EmailField(null=True)
    text = models.TextField(blank=True, null=False)
    rate = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(ProductFull, on_delete=models.CASCADE, related_name='reviews', null=True)

    def __str__(self):
        return f"Review by {self.author} for {self.product.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        product = self.product
        reviews = Review.objects.filter(product=product)
        average_rating = reviews.aggregate(Avg('rate'))['rate__avg']
        product.rating = average_rating
        product.save()