# admin.py
from django.contrib import admin
from .models import Category, MenuItem, Order

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Order)
