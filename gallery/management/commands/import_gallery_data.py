import json
import os
import uuid
from django.core.management.base import BaseCommand
from gallery.models import GalleryEntry

class Command(BaseCommand):
    help = 'Import gallery data from a JSON file in the static directory'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file', 
            type=str, 
            help="File name of the JSON file located in the static directory, e.g., 'gallery_entries.json'"
        )

    def handle(self, *args, **options):
        # Construct the full path to the file in the 'static' directory
        relative_path = options['json_file']
        json_file_path = os.path.join('static', relative_path)  # Direct reference to 'static' directory

        # Check if the file exists
        if not os.path.exists(json_file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {json_file_path}"))
            return

        # Load the JSON data
        try:
            with open(json_file_path, 'r') as file:
                entries = json.load(file)
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Invalid JSON format"))
            return

        # Process each entry in the JSON data
        for entry_data in entries:
            try:
                # Insert or update each GalleryEntry
                gallery_entry, created = GalleryEntry.objects.update_or_create(
                    id=uuid.UUID(entry_data.get('id')),  # Use UUID from JSON
                    defaults={
                        'nama_batik': entry_data.get('nama_batik'),
                        'deskripsi': entry_data.get('deskripsi'),
                        'asal_usul': entry_data.get('asal_usul'),
                        'makna': entry_data.get('makna'),
                        'foto': entry_data.get('foto')  # Directly set the path from JSON
                    }
                )
                action = "Created" if created else "Updated"
                self.stdout.write(self.style.SUCCESS(f"{action} GalleryEntry: {gallery_entry.nama_batik}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to process entry {entry_data.get('nama_batik')}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Data imported successfully from file: {relative_path}"))
