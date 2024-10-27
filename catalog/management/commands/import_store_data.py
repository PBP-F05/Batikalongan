import json
import uuid
from django.core.management.base import BaseCommand
from django.contrib.staticfiles.finders import find
from catalog.models import Store, Product

class Command(BaseCommand):
    help = 'Import store and product data from a JSON file located in the static directory'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file', 
            type=str, 
            help="Relative path to the JSON file within the static directory, e.g., 'json/batik_huza.json'"
        )

    def handle(self, *args, **options):
        # Locate the file within static files
        relative_path = options['json_file']
        json_file_path = find(relative_path)  # Locate the file in static

        if not json_file_path:
            self.stdout.write(self.style.ERROR(f"File not found in static files: {relative_path}"))
            return

        # Load the JSON data
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Invalid JSON format"))
            return

        # Extract store information
        store_data = data.get('store')
        if not store_data:
            self.stdout.write(self.style.ERROR("Missing 'store' data in JSON"))
            return

        # Create or update the Store object without altering the image path
        store, created = Store.objects.update_or_create(
            id=uuid.UUID(store_data.get('id')),  # Use the UUID from JSON
            defaults={
                'name': store_data.get('name'),
                'address': store_data.get('address'),
                'product_count': store_data.get('product_count'),
                'image': store_data.get('image')  # Directly set the path from JSON
            }
        )
        
        # Insert products without altering the image path
        products_data = data.get('products', [])
        for product_data in products_data:
            # Create each product and associate it with the store
            product, created = Product.objects.update_or_create(
                id=uuid.UUID(product_data.get('id')),  # Use UUID from JSON
                defaults={
                    'name': product_data.get('name'),
                    'price': product_data.get('price'),
                    'description': product_data.get('description'),
                    'image': product_data.get('image'),  # Directly set the path from JSON
                    'store': store
                }
            )
        
        # Update store's product count based on actual product entries
        store.product_count = store.product_set.count()
        store.save()

        self.stdout.write(self.style.SUCCESS(f"Data imported successfully from static file: {relative_path}"))
