from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Store, Product
from .forms import StoreForm, ProductForm
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed  
from django.core import serializers
from django.core.paginator import Paginator
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
import json
import logging
from django.views.decorators.http import require_http_methods
from.decorators import admin_required

def show_catalog(request):
    price_filter = request.GET.get('price_filter')

    # Filter produk berdasarkan harga
    if price_filter == 'above_100k':
        products = Product.objects.filter(price__gte=100000)  # Harga 100 ribu ke atas
    elif price_filter == 'below_or_equal_100k':
        products = Product.objects.filter(price__lte=100000)  # Harga 100 ribu ke bawah
    else:
        products = Product.objects.all()  # Semua produk jika tidak ada filter

    stores = Store.objects.all()
    
    # Tentukan berapa produk yang ditampilkan per halaman
    paginator = Paginator(products, 8)  # Gunakan 'products' yang sudah difilter
    page_number = request.GET.get('page')  # Ambil nomor halaman dari query params
    page_obj = paginator.get_page(page_number)  # Ambil objek halaman saat ini
    
    
    # Jika permintaan AJAX, kita kembalikan data JSON saja
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        products_html = render_to_string('catalog/products_list.html', {'page_obj': page_obj})
        return JsonResponse({'products_html': products_html})

    # Untuk permintaan biasa (GET) kembalikan halaman penuh
    context = {
        'stores': stores,
        'page_obj': page_obj,
    }
    return render(request, 'catalog/show_catalog.html', context)

def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = Product.objects.filter(store=store)  # Ambil semua produk terkait dengan store
    
    context = {
        'store': store,
        'products': products,
    }
    return render(request, 'catalog/store_detail.html', context)
logger = logging.getLogger(__name__)  # untuk debugging

@require_POST
@login_required
@admin_required
def create_store(request):
    try:
        # Get data from request.POST and request.FILES
        store_name = strip_tags(request.POST.get('name', '').strip())
        address = strip_tags(request.POST.get('address', '').strip())
        product_count = request.POST.get('product_count')
        image = request.FILES.get('image')

        # Validate required fields
        if not store_name or not address or product_count is None:
            return JsonResponse({"error": "All fields must be filled."}, status=400)

        # Validate product_count as a positive integer
        try:
            product_count = int(product_count)
            if product_count < 0:
                return JsonResponse({"error": "Product count must be a positive number."}, status=400)
        except ValueError:
            return JsonResponse({"error": "Product count must be an integer."}, status=400)

        # Save the new store with the image
        new_store = Store(name=store_name, address=address, product_count=product_count, image=image)
        new_store.save()

        return JsonResponse({
            "message": "Store successfully added.",
            "store": {
                "id": str(new_store.id),
                "name": new_store.name,
                "address": new_store.address,
                "product_count": new_store.product_count,
                "image_url": new_store.image.url
            }
        }, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid data."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@admin_required
@require_http_methods(["GET", "POST"])
def edit_store(request, store_id):
    try:
        store = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return JsonResponse({'error': 'Store not found'}, status=404)

    if request.method == 'GET':
        # Mengirim data toko dalam JSON sebagai respons GET
        return JsonResponse({
            'store': {
                'name': store.name,
                'address': store.address,
                'product_count': store.product_count
            }
        })

    elif request.method == 'POST':
        try:
            # Periksa apakah ada file yang diunggah
            if 'foto' in request.FILES:
                store.image = request.FILES['foto']
            
            # Ambil data dari request.POST (FormData)
            store.name = request.POST.get('name', store.name)
            store.address = request.POST.get('address', store.address)
            product_count = request.POST.get('product_count')
            
            # Validasi product_count agar merupakan bilangan bulat positif
            if product_count.isdigit() and int(product_count) > 0:
                store.product_count = int(product_count)
            else:
                return JsonResponse({'error': 'Total Produk harus berupa bilangan bulat positif.'}, status=400)

            store.save()
            return JsonResponse({'message': 'Store updated successfully'})
        
        except Exception as e:
            return JsonResponse({'error': f'Gagal memperbarui store: {str(e)}'}, status=500)

@csrf_exempt
@require_POST
@login_required
@admin_required
def delete_store(request, store_id):
    store = get_object_or_404(Store, id=store_id)

    try:
        store.delete()
        return JsonResponse({"message": "Store successfully deleted."}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
@csrf_exempt
@require_POST
@login_required
@admin_required
def add_product_to_store(request, store_id):
    try:
        store = Store.objects.get(id=store_id)

        # Get and sanitize text fields
        product_name = strip_tags(request.POST.get('name', '').strip())
        price = request.POST.get('price')
        description = strip_tags(request.POST.get('description', '').strip())
        image = request.FILES.get('foto')

        # Check for missing fields
        if not product_name or not price or not description or not image:
            return JsonResponse({"error": "All fields must be filled."}, status=400)

        # Validate price
        try:
            price = float(price)
            if price <= 0:
                return JsonResponse({"error": "Price must be a positive number."}, status=400)
        except ValueError:
            return JsonResponse({"error": "Invalid price format."}, status=400)

        # Create and save the new product
        new_product = Product(
            name=product_name,
            price=price,
            store=store,
            description=description,
            image=image
        )
        new_product.save()

        # Send a success response
        return JsonResponse({
            "message": "Product added successfully.",
            "product": {
                "id": str(new_product.id),
                "name": new_product.name,
                "price": new_product.price,
                "description": new_product.description,
                "image": new_product.image.url
            }
        }, status=201)

    except Store.DoesNotExist:
        return JsonResponse({"error": "Store not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@login_required
@admin_required
def edit_product(request, product_id):
    # Ambil produk berdasarkan ID, atau tampilkan 404 jika tidak ditemukan
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'GET':
        # Kirim data produk dalam JSON untuk ditampilkan di form
        product_data = {
            "id": str(product.id),
            "name": product.name,
            "price": product.price,
            "description": product.description,
            "image": product.image.url if product.image else '',
        }
        return JsonResponse({"product": product_data}, status=200)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            product_name = strip_tags(data.get('name', '').strip())
            price = data.get('price')
            description = strip_tags(data.get('description', '').strip())
            image_url = data.get('image_url', '')

            # Validasi semua field
            if not product_name or not price or not description or not image_url:
                return JsonResponse({"error": "All fields are required."}, status=400)

            # Validasi format harga
            try:
                price = float(price)
                if price <= 0:
                    return JsonResponse({"error": "Price must be a positive number."}, status=400)
            except ValueError:
                return JsonResponse({"error": "Invalid price format."}, status=400)

            # Perbarui produk dengan data baru
            product.name = product_name
            product.price = price
            product.description = description
            product.image = image_url
            product.save()

            # Kirim respons sukses
            return JsonResponse({
                "message": "Product updated successfully.",
                "product": {
                    "id": str(product.id),
                    "name": product.name,
                    "price": product.price,
                    "description": product.description,
                    "image": product.image.url
                }
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid data."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        # Balas dengan metode tidak diizinkan jika selain GET atau POST
        return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
@login_required
@require_POST
@admin_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        store_id = product.store.id
        product.delete()

        return JsonResponse({
            "message": "Product deleted successfully.",
            "store_id": store_id
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = Product.objects.filter(store=store)
    return render(request, 'catalog/store_detail.html', {
        'store': store,
        'products': products
    })

def product_list(request):
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products})

def show_xml(request):
    data = Product.objects.all()
    data_store = Store.objects.all()
    return HttpResponse(serializers.serialize("xml", data, data_store), content_type="application/xml")

def show_json(request):
    data_store = Store.objects.all()
    return HttpResponse(serializers.serialize("json", data_store), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    data_store = Store.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data, data_store), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    data_store = Store.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data, data_store), content_type="application/json")