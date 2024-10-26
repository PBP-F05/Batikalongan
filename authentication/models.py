from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ("user", "User"),
        ("atmin", "Atmin"),
    ]

    nama = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    deskripsi = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nama
