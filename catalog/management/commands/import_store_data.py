import json
import uuid
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from catalog.models import Store, Product

class Command(BaseCommand):
    help = 'Import store and product data from a JSON file in STATIC_ROOT'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file', 
            type=str, 
            help="Path to the JSON file relative to STATIC_ROOT, e.g., 'batik_huza.json'"
        )

    def handle(self, *args, **options):
        # Construct the full path to the file in STATIC_ROOT
        relative_path = options['json_file']
        json_file_path = os.path.join(settings.STATIC_ROOT, relative_path)

        # Check if the file exists in STATIC_ROOT
        if not os.path.exists(json_file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {json_file_path}"))
            return

        # Load the JSON data
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Invalid JSON format"))
            return

        # Process store and product data as usual
        store_data = data.get('store')
        if not store_data:
            self.stdout.write(self.style.ERROR("Missing 'store' data in JSON"))
            return

        store, created = Store.objects.update_or_create(
            id=uuid.UUID(store_data.get('id')),
            defaults={
                'name': store_data.get('name'),
                'address': store_data.get('address'),
                'product_count': store_data.get('product_count'),
                'image': store_data.get('image')
            }
        )
        
        # Insert products
        products_data = data.get('products', [])
        for product_data in products_data:
            product, created = Product.objects.update_or_create(
                id=uuid.UUID(product_data.get('id')),
                defaults={
                    'name': product_data.get('name'),
                    'price': product_data.get('price'),
                    'description': product_data.get('description'),
                    'image': product_data.get('image'),
                    'store': store
                }
            )

        # Update store's product count
        store.product_count = store.product_set.count()
        store.save()

        self.stdout.write(self.style.SUCCESS(f"Data imported successfully from file: {relative_path}"))
