from django.contrib import admin
from .models import ProductModel,RatingModel

# Register your models here.

admin.site.register(ProductModel)
admin.site.register(RatingModel)

