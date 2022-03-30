from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from APPS.cart.models import Cart, CartItem
from .services import get_cart_id

from django.core.exceptions import ObjectDoesNotExist

from APPS.store.models import Product


def add_cart_product(request, product_id):
    color = request.GET['color']
    # size = request.GET['size']

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
        
    return redirect('cart')    

def remove_cart_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = get_cart_id(request)
    cart = Cart.objects.get(cart_id=cart_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart') 

def delete_cart_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = get_cart_id(request)
    cart = Cart.objects.get(cart_id=cart_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    cart_item.delete()
    return redirect('cart') 

def cart(request, total=0, quantity=0, cart_items=None):
    cart_id = get_cart_id(request)
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=cart_id)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity )
            quantity += cart_item.quantity
        tax = 0.19 * total
        grand_total = total +tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }

    return render(request, 'cart/cart.html', context)