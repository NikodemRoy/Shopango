from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=48, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    descripiton = models.TextField(max_length=255, blank=True)
    image = models.ImageField(upload_to='categories_images', blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('products_by_category', kwargs={'category_slug' : self.slug})
        # return reverse('products_by_category', args=[self.slug])



    
