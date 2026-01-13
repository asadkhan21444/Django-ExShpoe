
# ===============================================================================
# from django import template

# register = template.Library()

# @register.filter(name='is_in_cart')
# def is_in_cart(product, cart):
#     if not cart:
#         return False
#     # keys are strings, convert to int safely
#     for id in cart.keys():
#         try:
#             if int(id) == product.id:
#                 return True
#         except:
#             continue
#     return False



# @register.filter
# def get_item(dictionary, key):
#     return dictionary.get(str(key), 0)
# =======================================================
from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    if not cart:
        return False
    for id in cart.keys():
        try:
            if int(id) == product.id:
                return True
        except:
            continue
    return False


# app/templatetags/cart.py

@register.filter(name='get_item')
def get_item(cart, product):
    if not cart:
        return 0
    # Handle both Product object and product ID (int/str)
    key = str(product.id) if hasattr(product, 'id') else str(product)
    return cart.get(key, 0)

@register.filter(name="price_total")
def price_total(cart, product):
    # Now 'cart' is the dictionary and 'product' is the object
    # We call get_item using the same order
    quantity = get_item(cart, product)
    return product.price * quantity


@register.filter(name='total_cart_price')
def total_cart_price(products, cart):
    sum = 0
    if products:
        for p in products:
            # Yahan order theek karein: (cart, p)
            sum += price_total(cart, p)
    return sum
