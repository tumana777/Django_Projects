from django.urls import path
from .views import (IndexView, maincategory_product_list, 
                    product_list, product_detail, 
                    cart, cart_add, item_clear, item_increment, 
                    item_decrement, cart_clear, checkout, order_list
                    )

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('categories/<str:maincategory_name>/', maincategory_product_list, name='maincategory_list'),
    path('categories/<str:maincategory_name>/<str:category_name>/', product_list, name='product_list'),
    path('categories/<str:maincategory_name>/<str:category_name>/id=<int:product_pk>/', product_detail, name='product_detail'),
    path('cart/', cart, name="cart_detail"),
    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', order_list, name='order_list'),
]