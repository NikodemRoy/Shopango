from random import choices
from unittest.util import _MAX_LENGTH
from django.db import models
from django.urls import reverse
from django.db.models import Avg, Count

from APPS.accounts.models import Account
from .managers import VariationManager

from APPS.categories.models import Category

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=2550, blank=True)
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='products_images')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    is_discounted = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modifited_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_date']


    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status= True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg =float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status= True).aggregate(count=Count('rating'))
        count = 0
        if reviews['count'] is not None:
            avg = int(reviews['count'])
        return avg

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'category_slug' : self.category.slug, 'product_slug' : self.slug })
        # return reverse('product_detail', args=[self.category.slug, self.slug])



class Variation(models.Model):
    variation_category_choice = (
        ('color', 'color'),
        ('size', 'size'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return str(self.variation_value)
        # return str(f"{self.product} - Variation: {self.varation_value}")


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=96, blank=True)
    review = models.TextField(max_length=480, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_gallery', blank=True)

    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'Product Gallery'