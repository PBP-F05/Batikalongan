from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    PERAN_CHOICES = [
        ("user", "User"),
        ("atmin", "atmin"),
    ]

    nama = models.CharField(max_length=255)
    peran = models.CharField(max_length=20, choices=PERAN_CHOICES)
    deskripsi = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nama
