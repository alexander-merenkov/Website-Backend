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