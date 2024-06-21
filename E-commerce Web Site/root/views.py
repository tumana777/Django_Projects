from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import MainCategory, Category, Product, Order, OrderItem, Watchlist
from django.views.generic import ListView
from django.utils import timezone
from cart.cart import Cart
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from django.contrib import messages


def index(request):
    maincategories = MainCategory.objects.all()
    products = Product.objects.all()
    context = {
        "maincategories": maincategories,
        "products": products
    }
    return render(request, "root/index.html", context)

def maincategory_product_list(request, maincategory_name):
    maincategory = MainCategory.objects.get(name=maincategory_name)
    categories = maincategory.category_set.all()
    products = Product.objects.filter(category__maincategory__name=maincategory_name)
    
    watchlist = []
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user).values_list('product_id', flat=True)
     
    context = {
        "maincategory": maincategory,
        "categories": categories,
        "products": products,
        "watchlist": watchlist
    }
    
    return render(request, "root/maincategories.html", context)

def product_list(request, maincategory_name, category_name):
    maincategory = get_object_or_404(MainCategory, name=maincategory_name)
    category = get_object_or_404(Category, name=category_name)
    products = category.product_set.all()
    
    watchlist = []
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    
    context = {
        "maincategory": maincategory,
        "category": category,
        "products": products,
        "watchlist": watchlist,
    }
    
    return render(request, "root/products.html", context)

def product_detail(request, maincategory_name, category_name, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    is_in_watchlist = False
    if request.user.is_authenticated:
        is_in_watchlist = Watchlist.objects.filter(user=request.user, product=product).exists()
    context = {
        "maincategory": MainCategory.objects.get(name=maincategory_name),
        "category": Category.objects.get(name=category_name),
        "product": product,
        "is_in_watchlist": is_in_watchlist
    }
    return render(request, "root/product_detail.html", context)

@login_required(login_url="login")
def cart(request):
    previous_url = request.META.get('HTTP_REFERER')
    go_back_url = previous_url if previous_url else reverse('index')
    return render(request, "root/cart.html", {'go_back_url': go_back_url})

@login_required(login_url="login")
def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    if product.quantity > 0:
        cart.add(product=product)
    else:
        messages.error(request, "This product is out of stock and cannot be added to the cart.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url="login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")

@login_required(login_url="login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")

@login_required(login_url="login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")

@login_required(login_url="login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

@login_required(login_url="login")
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

@login_required(login_url='login')
def purchase(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    quantity = 1
    
    if product.quantity >= quantity:
        total_price = product.price
        order = Order.objects.create(total_price=total_price, user=request.user)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )
        product.quantity -= quantity
        product.save()
        return redirect('order_confirmation', order_id=order.id)
    else:
        messages.error(request, "Sorry, this product is out of stock.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'root/order_confirmation.html', {'order': order})

@login_required(login_url="login")
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'root/order_list.html', {'orders': orders})

@login_required(login_url="login")
def add_to_watchlist(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    Watchlist.objects.get_or_create(user=request.user, product=product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url="login")
def remove_from_watchlist(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    watchlist_item = get_object_or_404(Watchlist, user=request.user, product=product)
    watchlist_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url="login")
def watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    return render(request, "root/watchlist.html", {"watchlist_items": watchlist_items})

@login_required(login_url="login")
def api_add_to_watchlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Watchlist.objects.get_or_create(user=request.user, product=product)
    return JsonResponse({'status': 'added'})

@login_required(login_url="login")
def api_remove_from_watchlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Watchlist.objects.filter(user=request.user, product=product).delete()
    return JsonResponse({'status': 'removed'})

@login_required(login_url='login')
def my_products(request):
    products = Product.objects.filter(owner=request.user)
    return render(request, "root/my_products.html", {"products": products})