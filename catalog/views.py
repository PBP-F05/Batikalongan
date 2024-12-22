from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Store, Product
from .forms import StoreForm, ProductForm
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed  
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
import json
import logging
from django.views.decorators.http import require_http_methods
from.decorators import admin_required
from flask import Flask, jsonify, request
from uuid import UUID

def product_list_json(request):
    page = request.GET.get('page', 1)
    products = Product.objects.select_related('store').all()  # Add select_related to get store info efficiently
    
    # Create product data with store information
    product_list = []
    for product in products:
        product_dict = {
            'pk': product.pk,
            'fields': {
                'name': product.name,
                'price': product.price,
                'image': product.image.url if product.image else '',
                'store_name': product.store.name,  # Include store name
                'store_location': product.store.address,  # Include store location
            }
        }
        product_list.append(product_dict)
    
    paginator = Paginator(product_list, 12)
    
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    
    return JsonResponse({
        'products': list(products_page),
        'has_next': products_page.has_next(),
        'has_previous': products_page.has_previous(),
        'num_pages': paginator.num_pages,
    })

def product_list_store_json(request, store_id):
    page = request.GET.get('page', 1)

    store = get_object_or_404(Store, pk=store_id)

    products = Product.objects.filter(store=store)

    product_list = []
    for product in products:
        product_dict = {
            'id': product.pk,
            'name': product.name,
            'price': product.price,
            'description' : product.description,
            'image': product.image.url if product.image else None,
            'store_id' : product.store.id,
            'store_name': product.store.name,
            'store_location': product.store.address,
        }
        product_list.append(product_dict)

    paginator = Paginator(product_list, 12)

    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    return JsonResponse({
        'products': list(products_page),
        'has_next': products_page.has_next(),
        'has_previous': products_page.has_previous(),
        'num_pages': paginator.num_pages,
    })

app = Flask(__name__)

# Data toko dummy untuk contoh
stores_data = [
    # Berikan data toko sesuai dengan yang dibutuhkan (contoh gambar, nama, alamat, jumlah produk)
]

# @app.route('/getStores', methods=['GET'])
# def get_stores(request):
#     page = int(request.GET.get('page', 1))
#     entries = Store.objects.all()
#     paginator = Paginator(entries, 3)  # 3 entries per page
#     page_obj = paginator.get_page(page)

#     data = serializers.serialize("json", page_obj.object_list)

#     # Return data along with pagination details
#     return JsonResponse({
#         "entries": data,
#         "has_next": page_obj.has_next(),
#         "has_previous": page_obj.has_previous(),
#     })

@app.route('/getStores', methods=['GET'])
def get_stores():
    page = int(request.args.get('page', 1))
    per_page = 3  # Tampilkan 3 toko per halaman
    start = (page - 1) * per_page
    end = start + per_page
    stores = stores_data[start:end]
    return jsonify({'stores': stores})


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
    products = Product.objects.filter(store=store)
    
    context = {
        'store_id': store.id,
        'store': store,
        'products': products,
    }
    return render(request, 'catalog/store_detail.html', context)
logger = logging.getLogger(__name__)  # untuk debugging

@require_POST
@login_required
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
                'product_count': store.product_count,
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
            product_count = request.POST.get('product_count', store.product_count)
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
@admin_required
def edit_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found.'}, status=404)

    if request.method == 'GET': # Data buat edit
        return JsonResponse({
            'product': {
                'name': product.name,
                'price': product.price,
                'description': product.description,
                'image': product.image.url if product.image else None
            }
        })

    elif request.method == 'POST':
        # Handle product update
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        if name:
            product.name = name
        if price:
            try:
                product.price = float(price)
                if product.price <= 0:
                    return JsonResponse({"error": "Price must be a positive number."}, status=400)
            except ValueError:
                return JsonResponse({"error": "Invalid price format."}, status=400)
        if description:
            product.description = description
        if image:
            product.image = image

        product.save()
        return JsonResponse({'message': 'Product updated successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


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
    product_list = Product.objects.all()  # Ambil semua produk
    page = request.GET.get('page', 1)  # Ambil nomor halaman dari query params
    paginator = Paginator(product_list, 16)  # 16 produk per halaman

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Cek jika request AJAX
        products_data = [
            {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'image_url': product.image.url if product.image else '',
            }
            for product in products
        ]
        return JsonResponse({
            'products': products_data,
            'has_next': products.has_next(),
            'has_previous': products.has_previous(),
            'num_pages': paginator.num_pages,
            'current_page': products.number,
        })

    return render(request, 'catalog/product_list.html', {'products': products})

def show_xml(request):
    data_store = Store.objects.all()
    return HttpResponse(serializers.serialize("xml", data_store), content_type="application/xml")

def show_xml_product(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data_store = Store.objects.all()
    return HttpResponse(serializers.serialize("json", data_store), content_type="application/json")

def show_json_product(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data_store = Store.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data_store), content_type="application/xml")

def show_xml_by_id_product(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data_store = Store.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data_store), content_type="application/json")

def show_json_by_id_product(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


# Flutter
@require_POST
@csrf_exempt
def create_store_flutter(request):
    name = request.POST.get("name")
    address = request.POST.get("address")
    product_count = request.POST.get("product_count")
    image = request.FILES.get("image")

    # Validasi input
    if not name:
        return JsonResponse({'message': 'Nama toko tidak boleh kosong'}, status=400)
    if not address:
        return JsonResponse({'message': 'Alamat toko tidak boleh kosong'}, status=400)
    if not product_count:
        return JsonResponse({'message': 'Jumlah produk tidak boleh kosong'}, status=400)
    if not image:
        return JsonResponse({'message': 'Gambar toko tidak boleh kosong'}, status=400)

    try:
        # Konversi jumlah produk ke integer
        product_count = int(product_count)

        # Buat toko baru
        new_store = Store(
            name=name,
            address=address,
            product_count=product_count,
            image=image
        )
        new_store.save()

        return JsonResponse({'message': 'Toko berhasil dibuat', 'store_id': new_store.id}, status=201)

    except ValueError:
        return JsonResponse({'message': 'Jumlah produk harus berupa angka'}, status=400)
    except Exception as e:
        return JsonResponse({'message': f'Gagal membuat toko: {e}'}, status=500)


@require_POST
@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        try:
            # Parse JSON body
            data = json.loads(request.body)
            
            # Retrieve the store by ID or raise an error
            try:
                store = Store.objects.get(id=data["store_id"])
            except Store.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Store not found"}, status=404)
            
            # Create a new product
            new_product = Product.objects.create(
                name=data["name"],
                price=float(data["price"]),
                image=data["image"],
                store=store  # Foreign key reference
            )
            
            new_product.save()
            return JsonResponse({"status": "success", "product_id": new_product.id}, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@csrf_exempt
def update_store_flutter(request, id):
    # Get the store object or return a 404 error
    store = get_object_or_404(Store, id=id)

    if request.method == "POST":
        try:
            # Parse JSON body
            data = json.loads(request.body.decode('utf-8'))

            # Update store fields if provided in the request
            name = data.get("name")
            address = data.get("address")
            product_count = data.get("product_count")
            image_path = data.get("image")  # Direct image file path

            if name:
                store.name = name
            if address:
                store.address = address
            if product_count is not None:  # Explicit None check for integer fields
                store.product_count = product_count

            # Handle image update (if file path is provided)
            if image_path:
                store.image = image_path

            # Save the updated store
            store.save()

            return JsonResponse({"status": "success", "message": "Store updated successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

def update_product_flutter(request, product_id):
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, pk=product_id)
            
            data = json.loads(request.body)
            
            name = data.get('name')
            price = data.get('price')

            if name:
                product.name = name
            if price:
                product.price = price

            if 'image' in request.FILES:
                product.image = request.FILES['image']

            product.save()

            return JsonResponse({
                'success': True,
                'message': 'Product updated successfully',
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image_url': product.image.url if product.image else None
                }
            }, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid HTTP method'}, status=405)

@require_POST
@csrf_exempt
def delete_store_flutter(request, store_id):
    try:
        store = Store.objects.get(id=store_id)
        store.delete()
        return JsonResponse({"message": "Toko berhasil dihapus"}, status=200)
    except Store.DoesNotExist:
        return JsonResponse({"message": "Toko tidak ditemukan"}, status=404)
    except Exception as e:
        return JsonResponse({"message": f"Gagal menghapus toko: {e}"}, status=500)

@require_POST
@csrf_exempt
def delete_product_flutter(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return JsonResponse({"message": "Produk berhasil dihapus"}, status=200)
    except Product.DoesNotExist:
        return JsonResponse({"message": "Produk tidak ditemukan"}, status=404)
    except Exception as e:
        return JsonResponse({"message": f"Gagal menghapus produk: {e}"}, status=500)
