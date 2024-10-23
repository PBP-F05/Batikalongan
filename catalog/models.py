from django.db import models

# Create your models here.
class Batik(models.Model):
    # Defining the fields for Batik model
    name = models.CharField(max_length=100, unique=True)  # Nama Batik
    motif = models.CharField(max_length=200)  # Motif Batik
    origin = models.CharField(max_length=100)  # Asal Batik (Kota / Provinsi)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Harga Batik
    stock = models.PositiveIntegerField()  # Stok Batik
    description = models.TextField(blank=True, null=True)  # Deskripsi opsional
    created_at = models.DateTimeField(auto_now_add=True)  # Waktu dibuat
    updated_at = models.DateTimeField(auto_now=True)  # Waktu di-update terakhir

    def __str__(self):
        return self.name  # Menampilkan nama batik di admin panel

    class Meta:
        ordering = ['-created_at']  # Mengurutkan berdasarkan waktu pembuatan (terbaru di atas)
