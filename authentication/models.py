from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    PERAN_CHOICES = [
        ("user", "User"),
        ("atmin", "atmin"),
    ]

    nama = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=PERAN_CHOICES)
    deskripsi = models.TextField(blank=True, null=True)

    # Avoid reverse accessor clashes with 'auth.User'
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='authentication_user_groups',  # Custom related_name
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=('groups'),
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='authentication_user_permissions',  # Custom related_name
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )

    def __str__(self):
        return self.nama
