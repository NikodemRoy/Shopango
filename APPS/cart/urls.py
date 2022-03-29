from django import views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.cart, name="cart"),
    path('add_product/<int:product_id>/', views.add_cart_product, name="add_product"),
    path('remove_product/<int:product_id>/', views.remove_cart_product, name="remove_product"),
    path('delete_product/<int:product_id>/', views.delete_cart_product, name="delete_product"),
]


