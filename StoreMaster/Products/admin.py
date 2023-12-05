from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductInCart)
admin.site.register(ProductInOrder)
admin.site.register(ProductInPurchase)