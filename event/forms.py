from django.forms import DateField, ModelForm
from event.models import Event

class EventForm(ModelForm):
    tanggal = DateField(input_formats=["%Y-%m-%d"])
    tanggal.widget.input_type = "date"

    class Meta:
        model = Event
        fields = ["nama", "deskripsi", "tanggal", "lokasi", "foto"]
