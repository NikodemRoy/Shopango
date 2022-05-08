from django import views
from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('', views.dashboard, name="dashboard"),


    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('reset-password/', views.resetPassword, name="resetpassword"),
    path('resetpassword-validate/<uidb64>/<token>/', views.resetpassword_validate, name="resetpassword_validate"),
    path('new-password/', views.new_password, name="new_password"),
]
