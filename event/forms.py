from django.forms import DateField, ImageField, ModelForm
from event.models import Event

class EventForm(ModelForm):
    tanggal = DateField(input_formats=["%Y-%m-%d"])
    tanggal.widget.input_type = "date"

    foto = ImageField(required=False)
    foto.widget.input_type = "file"

    class Meta:
        model = Event
        fields = ["nama", "deskripsi", "tanggal", "lokasi", "foto"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
