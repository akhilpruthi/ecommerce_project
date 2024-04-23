# from django.contrib import admin

from django.contrib import admin
from .models import Brand, UsageFor,Product

# Register your models here.
admin.site.register(Brand)
admin.site.register(UsageFor)
admin.site.register(Product)


