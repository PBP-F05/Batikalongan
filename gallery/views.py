from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from gallery.models import GalleryEntry
from gallery.forms import GalleryEntryForm

from django.shortcuts import render
from .models import GalleryEntry

def show_gallery(request):
    # Mengambil semua entri dari model GalleryEntry
    gallery_data = GalleryEntry.objects.all()
    
    # Mengirim data dari database ke template
    return render(request, 'gallery.html', {'gallery_data': gallery_data})




# View untuk menambahkan entri galeri baru
def add_gallery_entry(request):
    if request.method == 'POST':
        form = GalleryEntryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery:show_gallery')  # Redirect ke halaman galeri setelah berhasil menambahkan
    else:
        form = GalleryEntryForm()

    return render(request, 'add_gallery_entry.html', {'form': form})


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

# View untuk menghapus entri galeri
def delete_gallery_entry(request, id):
    entry = get_object_or_404(GalleryEntry, id=id)
    if request.method == 'POST':
        entry.delete()
        return redirect('gallery:show_gallery')
    return render(request, 'delete_gallery_entry.html', {'entry': entry})