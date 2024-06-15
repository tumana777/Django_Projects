from django.urls import path
from .views import (
                    add_product, load_form, fetch_categories, fetch_subcategories, success_page,
                    MainCategoryListView, CategoryListView, SubCategoryListView
                    )

urlpatterns = [
    path('', MainCategoryListView.as_view(), name='maincategory_list'),
    path('categories/<str:maincategory_name>/', CategoryListView.as_view(), name='category_list'),
    path('subcategories/<str:maincategory_name>/<str:category_name>/', SubCategoryListView.as_view(), name='subcategory_list'),
    path('add_product/', add_product, name='add_product'),
    path('load_form/', load_form, name='load_form'),
    path('fetch_categories/', fetch_categories, name='fetch_categories'),
    path('fetch_subcategories/', fetch_subcategories, name='fetch_subcategories'),
    path('success/', success_page, name='success_page'),
]