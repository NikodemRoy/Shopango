from APPS.cart.services import get_cart_id
from .models import Cart
from .models import CartItem

def cart_item_count(request):
    cart_count = 0
    if 'admin' in request.path:
        cart_count = 0
    else:
        try:
            cart = Cart.objects.filter(cart_id=get_cart_id(request))
            user = request.user
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    
    return {'cart_count':cart_count}