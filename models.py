from django.db import models
from django.conf import settings

class category(models.Model):
    cate=models.CharField(max_length=100,default='uncat')

class Product(models.Model):
    cat=models.ForeignKey(category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    price = models.IntegerField(default=0)

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='categories')
    name = models.CharField(max_length=100, default='')  # Default value added
    description = models.TextField(default='')  # Default value added
    price = models.IntegerField(default=0)  # Default value added
    
class WishItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,default='')
    description = models.TextField(default='')  # Default value added
    price = models.IntegerField(default=0)  # Default value added
