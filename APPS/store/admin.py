from django.contrib import admin
from .models import Product

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("product_name",)}
    list_display = ('product_name', 'price', 'stock', 'is_available', 'category', 'modifited_date')

admin.site.register(Product, CategoryAdmin)
# Register your models here.
