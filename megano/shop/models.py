from django.contrib.auth.models import User
from django.db import models
from products.models import ProductFull


class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Basket for {self.user.username}"


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey('products.ProductFull', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.count} x {self.product.title} in Basket {self.basket.id}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    createdAt = models.DateTimeField(null=True)
    fullName = models.CharField(max_length=100, null=True)
    email = models.EmailField()
    phone = models.CharField(verbose_name='phone number', max_length=16)
    deliveryType = models.CharField(max_length=20, blank=True)
    paymentType = models.CharField(max_length=20, blank=True)
    totalCost = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    status = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=100, null=True)
    products = models.ManyToManyField(ProductFull)

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"


class Orders(models.Model):
    class Meta:
        verbose_name = 'Orders History'
        verbose_name_plural = 'Orders Histories'

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return f'Orders for {self.user.username}'


class Discount(models.Model):
    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discount'

    express = models.DecimalField(max_digits=8, decimal_places=2)
    regular = models.DecimalField(max_digits=8, decimal_places=2)
    limit = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    def get_discount():
        return Discount.objects.first()

    def __str__(self):
        return 'Global Discount'