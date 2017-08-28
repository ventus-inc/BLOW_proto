from django.contrib import admin

# Register your models here.

from .models import Token, BuyOrder

admin.site.register(BuyOrder)
admin.site.register(Token)
