from django.urls import path
from event.views import show_event, create_event, edit_event, delete_event, create_event_ajax, get_events_json, create_event_flutter, edit_event_flutter

app_name = "event"

urlpatterns = [
    path("", show_event, name="show_event"),
    path("create", create_event, name="create_event"),
    path("create-ajax", create_event_ajax, name="create_event_ajax"),
    path("create-flutter/", create_event_flutter, name="create_event_flutter"),

    path("edit/<uuid:id>", edit_event, name="edit_event"),
    path("edit-flutter/<uuid:id>", edit_event_flutter, name="edit_event_flutter"),

    path("delete/<uuid:id>", delete_event, name="delete_event"),

    path("json/", get_events_json, name="get_events_json"),
    path("json/<uuid:id>", get_events_json, name="get_events_all_json"),
]
