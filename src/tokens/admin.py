from django.contrib import admin

# Register your models here.

from .models import BuyOrder

admin.site.register(BuyOrder)
