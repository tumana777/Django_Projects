from django import template

register = template.Library()


@register.filter()
def multiply(value, arg):
    return float(value) * arg

@register.filter
def total_quantity(cart):
    return sum(item['quantity'] for item in cart.values())