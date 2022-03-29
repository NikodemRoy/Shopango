from APPS.cart.services import get_cart_id
from .models import Cart
from .models import CartItem

def cart_item_count(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart_id = get_cart_id(request)
            cart = Cart.objects.get(cart_id=cart_id)
            cart_items = CartItem.objects.all().filter(cart=cart)

            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 99
    
    return {'cart_count':cart_count}