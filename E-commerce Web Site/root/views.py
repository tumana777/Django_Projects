from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import MainCategory, Category, Product, Order, OrderItem
from django.views.generic import ListView
from django.utils import timezone
from cart.cart import Cart
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from django.contrib import messages


class IndexView(ListView):
    model = MainCategory
    template_name = "root/index.html"
    context_object_name = "maincategories"

def maincategory_product_list(request, maincategory_name):
    maincategory = MainCategory.objects.get(name=maincategory_name)
    categories = maincategory.category_set.all()
    products = Product.objects.filter(category__maincategory__name=maincategory_name)
     
    context = {
        "maincategory": maincategory,
        "categories": categories,
        "products": products
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

@login_required
def cart(request):
    previous_url = request.META.get('HTTP_REFERER')
    go_back_url = previous_url if previous_url else reverse('index')
    return render(request, "root/cart.html", {'go_back_url': go_back_url})

@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    if product.quantity > 0:
        cart.add(product=product)
    else:
        messages.error(request, "This product is out of stock and cannot be added to the cart.")
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

@login_required
def checkout(request):
    user = request.user
    cart = Cart(request)
    cart_items = CartItem.objects.filter(user=user)
    if not cart_items.exists():
        return redirect('cart_detail')

    total_price = sum(item.quantity * item.price for item in cart_items)

    order = Order.objects.create(user=user, total_price=total_price, created_at=timezone.now())

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.price
        )
        item.product.quantity -= item.quantity
        item.product.save()

    cart.clear()

    return redirect('order_list')

@login_required(login_url="login")
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'root/order_list.html', {'orders': orders})