from django.contrib import admin

from APPS.cart.models import Cart, CartItem

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'id')

admin.site.register(Cart)
admin.site.register(CartItem, CartItemAdmin)
# Register your models here.
