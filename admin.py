from django.contrib import admin
from .models import Product, CartItem, WishItem, category

# Register your models here.
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(WishItem)
admin.site.register(category)