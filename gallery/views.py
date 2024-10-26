from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from gallery.models import GalleryEntry
from gallery.forms import GalleryEntryForm
from django.core.paginator import Paginator
from django.core import serializers

# Fungsi untuk menampilkan galeri dengan pagination
def show_gallery(request):
    return render(request, "gallery.html")
    
# Fungsi untuk menambah entri galeri
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

# Fungsi untuk menghapus entri galeri
def delete_gallery_entry(request, id):
    entry = get_object_or_404(GalleryEntry, id=id)
    if request.method == 'POST':
        entry.delete()
        return redirect('gallery:show_gallery')
    return render(request, 'delete_gallery_entry.html', {'entry': entry})

# Fungsi untuk mengembalikan semua entri galeri dalam format XML
def show_gallery_xml(request):
    data = GalleryEntry.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Fungsi untuk mengembalikan semua entri galeri dalam format JSON
def show_gallery_json(request):
    data = GalleryEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

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

@csrf_exempt
@require_POST
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
