from django import forms
from django.utils.html import strip_tags
from gallery.models import GalleryEntry

class GalleryEntryForm(forms.ModelForm):
    class Meta:
        model = GalleryEntry
        fields = ['nama_batik', 'deskripsi', 'makna', 'asal_usul', 'foto']
        widgets = {
            'nama_batik': forms.TextInput(attrs={
                'class': 'w-full border-2 border-[#D88E30] rounded-lg p-3',
                'placeholder': 'Masukkan nama batik'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'w-full border-2 border-[#D88E30] rounded-lg p-3',
                'placeholder': 'Masukkan deskripsi batik'
            }),
            'makna': forms.Textarea(attrs={
                'class': 'w-full border-2 border-[#D88E30] rounded-lg p-3',
                'placeholder': 'Masukkan makna batik'
            }),
            'asal_usul': forms.Textarea(attrs={
                'class': 'w-full border-2 border-[#D88E30] rounded-lg p-3',
                'placeholder': 'Masukkan asal-usul batik'
            }),
            'foto': forms.ClearableFileInput(attrs={
                'class': 'w-full border-2 border-dashed border-[#D88E30] rounded-lg p-3',
            }),
        }

    def clean_nama_batik(self):
        nama_batik = self.cleaned_data.get("nama_batik", "")
        return strip_tags(nama_batik)  # Remove HTML tags

    def clean_deskripsi(self):
        deskripsi = self.cleaned_data.get("deskripsi", "")
        return strip_tags(deskripsi)  # Remove HTML tags

    def clean_makna(self):
        makna = self.cleaned_data.get("makna", "")
        return strip_tags(makna)  # Remove HTML tags

    def clean_asal_usul(self):
        asal_usul = self.cleaned_data.get("asal_usul", "")
        return strip_tags(asal_usul)  # Remove HTML tags
