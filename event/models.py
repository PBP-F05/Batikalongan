import uuid
from django.db import models

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=50)
    deskripsi = models.TextField()
    tanggal = models.DateField()
    lokasi = models.CharField(max_length=50)
    foto = models.ImageField(upload_to="images/", blank=True)
