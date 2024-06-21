from django.urls import path
from .views import (index, maincategory_product_list, 
                    product_list, product_detail, 
                    cart, cart_add, item_clear, item_increment, 
                    item_decrement, cart_clear, checkout, 
                    order_list, watchlist, add_to_watchlist,
                    remove_from_watchlist, api_add_to_watchlist,
                    api_remove_from_watchlist, my_products, 
                    purchase, order_confirmation
                    )

urlpatterns = [
    path('', index, name='index'),
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
    path('purchase/<int:product_pk>/', purchase, name='purchase'),
    path('order-confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
    path('orders/', order_list, name='order_list'),
    path('watchlist/', watchlist, name='watchlist'),
    path('add_to_watchlist/<int:product_pk>/', add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<int:product_pk>/', remove_from_watchlist, name='remove_from_watchlist'),
    path('watchlist/api/add/<int:product_id>/', api_add_to_watchlist, name='api_add_to_watchlist'),
    path('watchlist/api/remove/<int:product_id>/', api_remove_from_watchlist, name='api_remove_from_watchlist'),
    path('my_products/', my_products, name='my_products'),
]