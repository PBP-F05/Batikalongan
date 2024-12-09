from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from gallery.models import GalleryEntry
from gallery.forms import GalleryEntryForm
from django.core.paginator import Paginator
from django.core import serializers

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import GalleryEntry
from .decorators import admin_required

# Fungsi untuk menampilkan galeri dengan pagination
def show_gallery(request):
    return render(request, "gallery.html")
    
# Fungsi untuk menambah entri galeri
# @admin_required
def add_gallery_entry(request):
    if request.method == 'POST':
        form = GalleryEntryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery:show_gallery')
    else:
        form = GalleryEntryForm()
    return render(request, 'add_gallery_entry.html', {'form': form})

# Fungsi untuk mengedit entri galeri
# @admin_required
def edit_gallery_entry(request, id):
    entry = get_object_or_404(GalleryEntry, id=id)
    if request.method == 'POST':
        form = GalleryEntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('gallery:show_gallery')
    else:
        form = GalleryEntryForm(instance=entry)
    return render(request, 'edit_gallery_entry.html', {'form': form, 'entry': entry})



# Fungsi untuk mengembalikan semua entri galeri dalam format XML
def show_gallery_xml(request):
    data = GalleryEntry.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Fungsi untuk mengembalikan entri galeri berdasarkan ID dalam format XML
def show_gallery_xml_by_id(request, id):
    data = GalleryEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Fungsi untuk mengembalikan entri galeri berdasarkan ID dalam format JSON
def show_gallery_json_by_id(request, id):
    data = GalleryEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse



def show_gallery_json(request):
    page = int(request.GET.get('page', 1))
    entries = GalleryEntry.objects.all()
    paginator = Paginator(entries, 6)  # 6 entries per page
    page_obj = paginator.get_page(page)

    data = serializers.serialize("json", page_obj.object_list)

    # Return data along with pagination details
    return JsonResponse({
        "entries": data,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
        "current_page": page_obj.number,
        "num_pages": paginator.num_pages,
    })


# @admin_required
def delete_gallery_entry(request, id):
    try:
        entry = get_object_or_404(GalleryEntry, id=id)
        entry.delete()
        return JsonResponse({'message': 'Deleted successfully'}, status=200)
    except Exception as e:
        print(f"Error deleting entry: {e}")
        return JsonResponse({'error': 'Failed to delete entry'}, status=500)

# @csrf_exempt
# @require_POST
# @admin_required
def add_gallery_entry_ajax(request):
    nama_batik = request.POST.get("nama_batik")
    deskripsi = request.POST.get("deskripsi")
    asal_usul = request.POST.get("asal_usul")
    makna = request.POST.get("makna")
    foto = request.FILES.get("foto")

    if nama_batik and deskripsi and asal_usul and makna and foto:
        new_entry = GalleryEntry(
            nama_batik=nama_batik,
            deskripsi=deskripsi,
            asal_usul=asal_usul,
            makna=makna,
            foto=foto
        )
        new_entry.save()
        return JsonResponse({'message': 'CREATED'}, status=201)
    return JsonResponse({'message': 'FAILED'}, status=400)

# @csrf_exempt
# @require_POST
# @admin_required
def edit_gallery_entry_ajax(request, id):
    entry = get_object_or_404(GalleryEntry, id=id)
    nama_batik = request.POST.get("nama_batik")
    deskripsi = request.POST.get("deskripsi")
    asal_usul = request.POST.get("asal_usul")
    makna = request.POST.get("makna")
    foto = request.FILES.get("foto")

    if nama_batik: entry.nama_batik = nama_batik
    if deskripsi: entry.deskripsi = deskripsi
    if asal_usul: entry.asal_usul = asal_usul
    if makna: entry.makna = makna
    if foto: entry.foto = foto

    entry.save()
    return JsonResponse({'message': 'Updated successfully'}, status=200)