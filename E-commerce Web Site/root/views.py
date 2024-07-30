from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpRequest
from django.template.loader import render_to_string
from .models import MainCategory, Category, Product, Order, OrderItem, Watchlist
from django.views.generic import View, ListView, TemplateView, UpdateView, DeleteView
from django.utils import timezone
from cart.cart import Cart
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

class IndexView(ListView):
    model = Product
    template_name = 'root/index.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("query")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        
        queryset = Product.objects.all()
        
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        if min_price:
            queryset = queryset.filter(Q(price__gte=min_price))
        if max_price:
            queryset = queryset.filter(Q(price__lte=max_price))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        if query:
            context['total_products'] = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)).count()
        elif min_price:
            context['total_products'] = Product.objects.filter(Q(price__gte=min_price)).count()
        elif max_price:
            context['total_products'] = Product.objects.filter(Q(price__lte=max_price)).count()
        else:
            context['total_products'] = Product.objects.count()

        context['maincategories'] = MainCategory.objects.all()
        context['query'] = query or ""
        context['min_price'] = min_price or ""
        context['max_price'] = max_price or ""
        
        return context



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

class MyProductsListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "root/my_products.html"
    context_object_name = "products"
    login_url = 'login'
    
    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_products"] = self.get_queryset().count()
        return context

def seller_products(request, seller_name):
    seller = User.objects.get(username=seller_name)
    products = Product.objects.filter(seller=seller)
    total_products = len(products)
    return render(request, "root/seller_products.html", {"seller": seller,"products": products, "total_products": total_products})

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ["name", "description", "price", "quantity", "image"]
    template_name = "root/product_update.html"
    success_url = reverse_lazy('my_products')
    
    def test_func(self):
        product = self.get_object()
        if self.request.user == product.seller:
            return True
        return False

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    login_url = 'login'
    success_url = reverse_lazy('my_products')
    
    def test_func(self):
        product = self.get_object()
        if self.request.user == product.seller:
            return True
        return False