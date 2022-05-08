from django.contrib import admin
from .models import Product, Variation

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("product_name",)}
    list_display = ('product_name', 'price', 'stock', 'is_available', 'category', 'modifited_date', 'id')

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'id')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value',)

admin.site.register(Variation, VariationAdmin)
admin.site.register(Product, ProductAdmin)
# Register your models here.
