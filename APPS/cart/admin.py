from django.contrib import admin

from APPS.cart.models import Cart, CartItem
from APPS.store.models import ReviewRating

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'id')

admin.site.register(Cart)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(ReviewRating)
# Register your models here.
