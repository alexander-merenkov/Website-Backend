from django.contrib import admin
from .models import Basket, BasketItem, Order


class BasketItemInline(admin.TabularInline):
    model = BasketItem
    extra = 0


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    inlines = [BasketItemInline]


admin.site.register(BasketItem)
admin.site.register(Order)


