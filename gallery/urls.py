from django.urls import path
from .views import show_gallery, add_gallery_entry, edit_gallery_entry, delete_gallery_entry

app_name = 'gallery'

urlpatterns = [
    path('', show_gallery, name='show_gallery'),
    path('add/', add_gallery_entry, name='add_gallery_entry'),
    path('edit/<uuid:id>/', edit_gallery_entry, name='edit_gallery_entry'),  # UUID karena id adalah UUIDField
    path('delete/<uuid:id>/', delete_gallery_entry, name='delete_gallery_entry'),
]
