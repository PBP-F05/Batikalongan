# catalog/models.py
from django.db import models
import uuid

class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    product_count = models.IntegerField()

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    
    def __str__(self):
        return self.name
