from django import views
from django.urls import path

from . import views

urlpatterns = [
    path('place_order/', views.place_order, name="place_order"),
    path('payment/', views.payment, name="payment"),
    path('order_complite/', views.order_complite, name="order_complite"),
]