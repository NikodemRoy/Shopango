from email.policy import default
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomAccountManager

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Account(AbstractBaseUser):
    username = None
    email = models.EmailField(('email address'), unique=True, db_index=True)
    
    first_name = models.CharField(max_length=48)
    last_name = models.CharField(max_length=48)
    phone_number = PhoneNumberField(null=True, blank=True, unique=False)

    created_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    objects = CustomAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, add_label):
        return True
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, db_index=True)
    addres_1 = models.CharField(max_length=96, blank=True)
    addres_2 = models.CharField(max_length=96, blank=True)
    profile_picture = models.ImageField(upload_to='user_profiles', default='user_profiles/default.png')
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'{self.addres_1} {self.addres_2}'
