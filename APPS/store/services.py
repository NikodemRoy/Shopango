from django.db.models import Q

from APPS.store.models import Product

def get_search(request):
    products = None
    product_count = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(
            Q(product_name__icontains= keyword)|
            Q(slug__icontains= keyword)|
            Q(description__icontains= keyword),
            is_available=True)

            product_count = products.count()

    return products, product_count