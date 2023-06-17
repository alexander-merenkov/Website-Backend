from django.contrib import admin
from .models import Basket, BasketItem, Order, Orders, Discount, Payment


class PaymentInLine(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(Order)
class PaymentAdmin(admin.ModelAdmin):
    inlines = [PaymentInLine]


class BasketItemInline(admin.TabularInline):
    model = BasketItem
    extra = 0


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    inlines = [BasketItemInline]


class DiscountAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Discount, DiscountAdmin)
admin.site.register(BasketItem)
admin.site.register(Payment)
admin.site.register(Orders)



