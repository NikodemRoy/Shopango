from unicodedata import category
from django.shortcuts import get_object_or_404, render

from APPS.categories.models import Category

from .models import Product

# Create your views here.

def home(request):
    products = Product.objects.all().filter(is_available=True)
    context = {'products':products}
    return render(request, 'store/home.html', context)


def store(request, category_slug=None):
    category = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True )
        product_count = products.count()

    else:    
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    context = {'products':products, 'product_count':product_count}
    return render(request, 'store/store.html', context )

def product_detail(request, category_slug, product_slug):
    # category = get_object_or_404(Category, slug=category_slug)
    # single_product = Product.objects.get(category=category, slug=product_slug)

    single_product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug )

    context = {'single_product':single_product}
    return render(request, 'store/product_detail.html', context )