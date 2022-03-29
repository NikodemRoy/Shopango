from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from .services import get_search
from APPS.cart.models import CartItem
from APPS.cart.services import get_cart_id
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
        
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)


    else:    
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()
        
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)


    context = {'products':paged_products, 'product_count':product_count,}

    return render(request, 'store/store.html', context )

def product_detail(request, category_slug, product_slug):
    single_product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug )
    cart_id = get_cart_id(request)
    
    in_cart = CartItem.objects.filter(cart__cart_id=cart_id, product= single_product).exists()
  
    context = {'single_product':single_product, 'in_cart':in_cart}
    return render(request, 'store/product_detail.html', context )

def search(request):
    products, product_count = get_search(request)
    
    context = {'products':products, 'product_count':product_count,}
    return render(request, 'store/store.html', context )