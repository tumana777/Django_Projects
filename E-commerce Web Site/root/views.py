from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import MainCategory, Category, Product
from django.views.generic import ListView
from cart.cart import Cart
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


class IndexView(ListView):
    model = MainCategory
    template_name = "root/index.html"
    context_object_name = "maincategories"

def maincategory_product_list(request, maincategory_name):
    maincategory = MainCategory.objects.get(name=maincategory_name)
    categories = maincategory.category_set.all()
    
    context = {
        "maincategory": maincategory,
        "categories": categories
    }
    
    return render(request, "root/maincategories.html", context)

def product_list(request, maincategory_name, category_name):
    maincategory = MainCategory.objects.get(name=maincategory_name)
    category = Category.objects.get(name=category_name)
    
    context = {
        "maincategory": maincategory,
        "category": category
    }
    
    return render(request, "root/products.html", context)

def product_detail(request, maincategory_name, category_name, product_pk):
    product = Product.objects.get(pk=product_pk)
    context = {
        "maincategory": MainCategory.objects.get(name=maincategory_name),
        "category": Category.objects.get(name=category_name),
        "product": product
    }
    return render(request, "root/product_detail.html", context)

login_required
def cart(request):
    previous_url = request.META.get('HTTP_REFERER')
    go_back_url = previous_url if previous_url else reverse('index')
    return render(request, "root/cart.html", {'go_back_url': go_back_url})

@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")