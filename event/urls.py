from django.urls import path
from event.views import show_event, create_event, edit_event, delete_event, create_event_ajax

app_name = "event"

urlpatterns = [
    path("", show_event, name="show_event"),
    path("create", create_event, name="create_event"),
    path("create-ajax", create_event_ajax, name="create_event_ajax"),
    path("edit/<uuid:id>", edit_event, name="edit_event"),
    path("delete/<uuid:id>", delete_event, name="delete_event"),
]
