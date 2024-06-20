from decimal import Decimal
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import CartItem


class Cart(object):

    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.user = request.user if request.user.is_authenticated else None
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        if self.user:
            self.load_cart_from_db()

    def load_cart_from_db(self):
        cart_items = CartItem.objects.filter(user=self.user)
        for item in cart_items:
            self.cart[str(item.product.id)] = {
                'userid': item.user.id,
                'product_id': item.product.id,
                'name': item.product.name,
                'quantity': item.quantity,
                'price': str(item.price),
                'image_url': item.product.image.url if item.product.image else ''  # Ensure correct key
            }
        self.save()

    def add(self, product, quantity=1, action=None):
        if product.quantity <= 0:
            return  # Do not add the product if the quantity is zero or less

        id = product.id
        if str(product.id) not in self.cart.keys():
            self.cart[product.id] = {
                'userid': self.request.user.id,
                'product_id': id,
                'name': product.name,
                'quantity': 1,
                'price': str(product.price),
                'image_url': product.image.url if product.image else ''  # Ensure correct key
            }
        else:
            for key, value in self.cart.items():
                if key == str(product.id):
                    if value['quantity'] < product.quantity:
                        value['quantity'] += 1
                    self.save()
                    break
            else:
                self.cart[product.id] = {
                    'userid': self.request.user.id,
                    'product_id': product.id,
                    'name': product.name,
                    'quantity': 1,
                    'price': str(product.price),
                    'image_url': product.image.url if product.image else ''  # Ensure correct key
                }
        self.save()
        if self.user:
            self.save_to_db(product, quantity)

    def save_to_db(self, product, quantity):
        item, created = CartItem.objects.get_or_create(user=self.user, product=product)
        if not created:
            item.quantity += quantity
        item.price = product.price
        item.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
        if self.user:
            CartItem.objects.filter(user=self.user, product=product).delete()

    def decrement(self, product):
        for key, value in self.cart.items():
            if key == str(product.id):
                value['quantity'] -= 1
                if value['quantity'] < 1:
                    del self.cart[key]
                self.save()
                if self.user:
                    item = CartItem.objects.get(user=self.user, product=product)
                    if item.quantity > 1:
                        item.quantity -= 1
                        item.save()
                    else:
                        item.delete()
                break
            else:
                print("Something Wrong")

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
        if self.user:
            CartItem.objects.filter(user=self.user).delete()