from django.forms import ModelForm
from catalog.models import Store, Product

class StoreForm(ModelForm):
    class Meta:
        store = Store
        fields = ["name", "address", "product_count", "image"]

class ProductForm(ModelForm):
    class Meta:
        product = Product
        fields = ["name", "price", "description", "image"]