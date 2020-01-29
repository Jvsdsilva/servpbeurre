from django.contrib import admin

# Register your models here.
from aliments.models import Category
from aliments.models import Store
from aliments.models import Products
from aliments.models import Foodsave

admin.site.register(Category)
admin.site.register(Store)
admin.site.register(Products)
admin.site.register(Foodsave)
