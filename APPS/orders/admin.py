from django.contrib import admin

from APPS.orders.models import Payment, Order, OrderProduct

admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderProduct)
# Register your models here.
