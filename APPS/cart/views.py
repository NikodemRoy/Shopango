from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from APPS.cart.models import Cart, CartItem
from .services import get_cart_id
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist

from APPS.store.models import Product, Variation


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart_id = get_cart_id(request)
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:       
            cart = Cart.objects.get(cart_id=cart_id)
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity )
            quantity += cart_item.quantity
        tax = 0.19 * total
        grand_total = total
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

def add_cart_product(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    cart_id = get_cart_id(request)

    product_variations = []

    if current_user.is_authenticated:
        if request.method == 'POST':
            product = Product.objects.get(id=product_id)
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value )
                    product_variations.append(variation)
                except:
                    pass


        does_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()

        if does_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            created_variation_list = []
            id = []
            for item in cart_item:
                created_variation = item.variations.all()
                created_variation_list.append(list(created_variation))
                id.append(item.id)

            if product_variations in created_variation_list:
                index = created_variation_list.index(product_variations)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variations) > 0:
                    item.variations.clear()
                    for variation in product_variations:
                        item.variations.add(variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variations) > 0:
                for variation in product_variations:
                    cart_item.variations.add(variation)
            cart_item.save()

    else:
        if request.method == 'POST':
            product = Product.objects.get(id=product_id)
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value )
                    product_variations.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id=cart_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = cart_id
            )
        cart.save()

        does_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

        if does_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            created_variation_list = []
            id = []
            for item in cart_item:
                created_variation = item.variations.all()
                created_variation_list.append(list(created_variation))
                id.append(item.id)

            if product_variations in created_variation_list:
                index = created_variation_list.index(product_variations)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variations) > 0:
                    item.variations.clear()
                    for variation in product_variations:
                        item.variations.add(variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variations) > 0:
                for variation in product_variations:
                    cart_item.variations.add(variation)
            cart_item.save()
            
    return redirect('cart')    

def remove_cart_product(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart_id = get_cart_id(request)
            cart = Cart.objects.get(cart_id=cart_id)
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart') 

def delete_cart_product(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.filter(product=product, user=request.user, id=cart_item_id)
        else:   
            cart_id = get_cart_id(request)
            cart = Cart.objects.get(cart_id=cart_id)
            cart_item = CartItem.objects.filter(product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
    except:
        pass
    return redirect('cart') 

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        cart_id = get_cart_id(request)
        tax = 0
        grand_total = 0
        # cart = Cart.objects.get(cart_id=cart_id)
        # cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            user = request.user
        else:       
            cart = Cart.objects.get(cart_id=cart_id)
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity )
            quantity += cart_item.quantity
        tax = 0.19 * total
        grand_total = total
    except ObjectDoesNotExist:
        pass

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        'user': user
    }
    return render(request, 'cart/checkout.html', context)