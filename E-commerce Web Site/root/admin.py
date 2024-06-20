from django.contrib import admin
from .models import MainCategory, Category, Product, Order, OrderItem, Watchlist

admin.site.register(MainCategory)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Watchlist)