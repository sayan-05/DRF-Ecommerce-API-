from django.contrib import admin
from .models import ProductInfo, OrderItem, BoughtItem
# Register your models here.

admin.site.register(ProductInfo)
admin.site.register(OrderItem)
admin.site.register(BoughtItem)
