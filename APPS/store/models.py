from django.db import models
from django.urls import reverse

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


    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'category_slug' : self.category.slug, 'product_slug' : self.slug })
        # return reverse('product_detail', args=[self.category.slug, self.slug])