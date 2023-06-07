from django.contrib import admin
from .models import ProductFull, Review, Category, Image, Tag, Specifications

admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(ProductFull)
admin.site.register(Review)
admin.site.register(Specifications)

