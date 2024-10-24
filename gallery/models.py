import uuid
import os
from django.db import models

# Fungsi untuk mengganti nama file berdasarkan UUID
def rename_foto(instance, filename):
    # Ekstrak ekstensi file, misal .jpg atau .png
    ext = filename.split('.')[-1]
    
    # Gunakan UUID dari instance sebagai nama file
    filename = f"{instance.id}.{ext}"
    
    # Return path tempat file akan disimpan
    return os.path.join('gallery/batik_images/', filename)

class GalleryEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_batik = models.CharField(max_length=255)
    deskripsi = models.TextField()
    asal_usul = models.TextField()
    makna = models.TextField()
    foto = models.ImageField(upload_to=rename_foto)  # Gunakan fungsi rename_foto

    def __str__(self):
        return self.nama_batik
