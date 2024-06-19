from django.urls import path
from .views import (IndexView, maincategory_product_list, 
                    product_list, product_detail, 
                    cart, cart_add, item_clear, item_increment, 
                    item_decrement, cart_clear
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
    # path('add_product/', add_product, name='add_product'),
    # path('load_form/', load_form, name='load_form'),
    # path('fetch_categories/', fetch_categories, name='fetch_categories'),
    # path('fetch_subcategories/', fetch_subcategories, name='fetch_subcategories'),
    # path('success/', success_page, name='success_page'),
]