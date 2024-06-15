from django.contrib import admin
from .models import MainCategory, Category, SubCategory, Year, Storage, RAM

admin.site.register(MainCategory)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Year)
admin.site.register(Storage)
admin.site.register(RAM)

