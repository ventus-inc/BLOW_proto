from django.contrib import admin

# Register your models here.

from .models import TokenBoard, Token, BuyOrders

admin.site.register(BuyOrders)
