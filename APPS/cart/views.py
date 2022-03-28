from django.http import HttpResponse
from django.shortcuts import redirect, render
from APPS.cart.models import Cart, CartItem
from .services import get_cart_id

from APPS.store.models import Product

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_id = get_cart_id(request)
    try:
        cart = Cart.objects.get(cart_id=cart_id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = cart_id
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    return HttpResponse(f"Item:{cart_item.product}, Cart session ID: {cart.cart_id}")
    # return redirect('cart')    



def cart(request):
    context = {}

    return render(request, 'cart/cart.html', context)