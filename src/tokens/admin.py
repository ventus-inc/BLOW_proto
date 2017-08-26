from django.contrib import admin

# Register your models here.

from .models import TokenBoard, Token, BuyOrder

admin.site.register(BuyOrder)
