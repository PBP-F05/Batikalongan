from django.urls import path
from .views import (
    show_gallery, add_gallery_entry, edit_gallery_entry, delete_gallery_entry,
    show_gallery_xml, show_gallery_json, show_gallery_xml_by_id, show_gallery_json_by_id,
    add_gallery_entry_ajax, edit_gallery_entry_ajax,
    add_gallery_entry_flutter, edit_gallery_entry_flutter, delete_gallery_flutter
)

app_name = 'gallery'

urlpatterns = [
    path('', show_gallery, name='show_gallery'),
    path('add/', add_gallery_entry, name='add_gallery_entry'),
    path('edit/<uuid:id>/', edit_gallery_entry, name='edit_gallery_entry'),
    path('delete/<uuid:id>/', delete_gallery_entry, name='delete_gallery_entry'),
    path('xml/', show_gallery_xml, name='show_gallery_xml'),
    path('json/', show_gallery_json, name='show_gallery_json'),
    path('xml/<uuid:id>/', show_gallery_xml_by_id, name='show_gallery_xml_by_id'),
    path('json/<uuid:id>/', show_gallery_json_by_id, name='show_gallery_json_by_id'),
    path('add/ajax/', add_gallery_entry_ajax, name='add_gallery_entry_ajax'),
    path('edit/<uuid:id>/ajax/', edit_gallery_entry_ajax, name='edit_gallery_entry_ajax'),
    path('add/flutter/', add_gallery_entry_flutter, name='add_gallery_entry_flutter'),
    path('edit/<uuid:id>/flutter/', edit_gallery_entry_flutter, name='edit_gallery_entry_flutter'),
    path('delete/<uuid:id>/flutter/', delete_gallery_flutter, name='delete_gallery_flutter'),
]
