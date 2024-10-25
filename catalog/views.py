from django.shortcuts import render
from .models import Store, Product

def show_catalog(request):
    stores = Store.objects.all()
    products = Product.objects.all()
    context = {
        'stores': stores,
        'products': products,
    }
    return render(request, 'catalog/show_catalog.html', context)
