from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Store, Product
from .forms import StoreForm, ProductForm
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.paginator import Paginator
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
import json

def is_admin(user):
    return user.is_staff

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

@csrf_exempt
@require_POST
@login_required
def create_store(request):
    if not request.user.is_staff:  # Hanya admin yang bisa menambah toko
        return JsonResponse({"error": "Permission denied."}, status=403)

    try:
        data = json.loads(request.body.decode('utf-8'))

        # Ambil dan validasi data yang diterima dari AJAX
        store_name = strip_tags(data.get('name', '').strip())
        address = strip_tags(data.get('address', '').strip())
        product_count = data.get('product_count')

        if not store_name or not address or product_count is None:
            return JsonResponse({"error": "All fields must be filled."}, status=400)

        # Validasi product_count agar merupakan angka positif
        try:
            product_count = int(product_count)
            if product_count < 0:
                return JsonResponse({"error": "Product count must be a positive number."}, status=400)
        except ValueError:
            return JsonResponse({"error": "Invalid product count."}, status=400)

        # Membuat toko baru
        new_store = Store(
            name=store_name,
            address=address,
            product_count=product_count
        )
        new_store.save()

        # Kirim respons sukses dalam format JSON
        return JsonResponse({
            "message": "Store successfully added.",
            "store": {
                "id": new_store.id,
                "name": new_store.name,
                "address": new_store.address,
                "product_count": new_store.product_count
            }
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid data."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
@require_POST
@login_required
def edit_store(request, store_id):
    if not request.user.is_staff:  # Hanya admin yang dapat mengedit toko
        return JsonResponse({"error": "Permission denied."}, status=403)

    store = get_object_or_404(Store, id=store_id)

    try:
        data = json.loads(request.body.decode('utf-8'))

        # Ambil dan validasi data yang diterima dari AJAX
        store_name = strip_tags(data.get('name', '').strip())
        address = strip_tags(data.get('address', '').strip())
        product_count = data.get('product_count')

        if not store_name or not address or product_count is None:
            return JsonResponse({"error": "All fields must be filled."}, status=400)

        # Validasi product_count agar merupakan angka positif
        try:
            product_count = int(product_count)
            if product_count < 0:
                return JsonResponse({"error": "Product count must be a positive number."}, status=400)
        except ValueError:
            return JsonResponse({"error": "Invalid product count."}, status=400)

        # Update data store
        store.name = store_name
        store.address = address
        store.product_count = product_count
        store.save()

        # Kirim respons sukses dalam format JSON
        return JsonResponse({
            "message": "Store successfully updated.",
            "store": {
                "id": store.id,
                "name": store.name,
                "address": store.address,
                "product_count": store.product_count
            }
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid data."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
# Fungsi untuk menghapus toko
@csrf_exempt
@require_POST
@login_required
def delete_store(request, store_id):
    if not request.user.is_staff:
        return JsonResponse({"error": "Permission denied."}, status=403)

    store = get_object_or_404(Store, id=store_id)

    try:
        store.delete()

        # Kirim respon sukses dalam format JSON
        return JsonResponse({"message": "Store successfully deleted."}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_POST
@login_required
def add_product_to_store(request, store_id):
    if not request.user.is_staff:
        return JsonResponse({"error": "Permission denied."}, status=403)

    try:
        store = Store.objects.get(id=store_id)  # Get store by ID

        data = json.loads(request.body.decode('utf-8'))

        # Ekstrak data
        product_name = strip_tags(data.get('name', '').strip())
        price = data.get('price')
        description = strip_tags(data.get('description', '').strip())
        image_url = data.get('image_url', '')

        # Cek data terisi
        if not product_name or not price or not description or not image_url:
            return JsonResponse({"error": "All fields must be filled."}, status=400)

        # Validasi harga
        try:
            price = float(price)
            if price <= 0:
                return JsonResponse({"error": "Harga harus bilangan positif."}, status=400)
        except ValueError:
            return JsonResponse({"error": "Format harga tidak valid."}, status=400)

        # Buat produk baru yang terhubung ke toko
        new_product = Product(
            name=product_name,
            price=price,
            store=store,
            description=description,
            image=image_url
        )
        new_product.save()

        # Pesan jika berhasil
        return JsonResponse({
            "message": "Produk berhasil ditambahkan.",
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

    except json.JSONDecodeError:
        return JsonResponse({"error": "Data format tidak valid."}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_POST
@login_required
def edit_product(request, product_id):
    # Mendapatkan produk berdasarkan ID
    product = get_object_or_404(Product, id=product_id)

    # Validasi apakah user adalah admin atau staff
    if not request.user.is_staff:
        return JsonResponse({"error": "Permission denied."}, status=403)

    try:
        data = json.loads(request.body.decode('utf-8'))

        # Ambil data dari request dan lakukan sanitasi
        product_name = data.get('name', '').strip()
        price = data.get('price', '')
        description = data.get('description', '').strip()
        image_url = data.get('image_url', '')

        # Validasi bahwa semua field diisi
        if not product_name or not price or not description or not image_url:
            return JsonResponse({"error": "Semua kolom harus diisi."}, status=400)

        # Validasi format harga
        try:
            price = float(price)
            if price <= 0:
                return JsonResponse({"error": "Harga harus berupa angka positif."}, status=400)
        except ValueError:
            return JsonResponse({"error": "Format harga tidak valid."}, status=400)

        # Update produk dengan data yang baru
        product.name = product_name
        product.price = price
        product.description = description
        product.image = image_url  # Menyimpan URL gambar (diasumsikan disediakan oleh frontend)

        product.save()  # Simpan perubahan produk

        return JsonResponse({
            "message": "Produk berhasil diperbarui.",
            "product": {
                "id": str(product.id),
                "name": product.name,
                "price": product.price,
                "description": product.description,
                "image": product.image.url
            }
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Data tidak valid."}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@login_required
@require_POST
def delete_product(request, product_id):
    # Mendapatkan produk berdasarkan ID
    product = get_object_or_404(Product, id=product_id)

    # Validasi apakah user adalah staff atau admin
    if not request.user.is_staff:
        return JsonResponse({"error": "Permission denied."}, status=403)

    try:
        store_id = product.store.id  # Ambil ID toko terkait untuk keperluan pengalihan setelah penghapusan
        product.delete()  # Menghapus produk

        # Kirim respons sukses setelah penghapusan produk
        return JsonResponse({
            "message": "Produk berhasil dihapus.",
            "store_id": store_id
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = store.product_set.all()  # Mengambil semua produk yang terkait dengan toko
    
    context = {
        'store': store,
        'products': products,
    }
    return render(request, 'catalog/store_detail.html', context)

def product_list(request):
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products})

def show_xml(request):
    data = Product.objects.all()
    data_store = Store.objects.all()
    return HttpResponse(serializers.serialize("xml", data, data_store), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    data_store = Store.objects.all()
    return HttpResponse(serializers.serialize("json", data, data_store), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    data_store = Store.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data, data_store), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    data_store = Store.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data, data_store), content_type="application/json")