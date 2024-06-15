from django.urls import path
from . import views

urlpatterns = [
    path('add_product/', views.add_product, name='add_product'),
    path('load_form/', views.load_form, name='load_form'),
    path('fetch_categories/', views.fetch_categories, name='fetch_categories'),
    path('fetch_subcategories/', views.fetch_subcategories, name='fetch_subcategories'),
    path('success/', views.success_page, name='success_page'),
]