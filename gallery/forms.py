from django import forms
from gallery.models import GalleryEntry

class GalleryEntryForm(forms.ModelForm):
    class Meta:
        model = GalleryEntry
        fields = ['nama_batik', 'deskripsi', 'asal_usul', 'makna', 'foto']
