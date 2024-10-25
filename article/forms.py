from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'image', 'introduction', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'self-stretch h-[58px] rounded-lg border border-[#d88e30] px-4',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'hidden',  # Ini bisa tetap untuk menyembunyikan input file, tetapi pastikan labelnya ditampilkan
                'accept': 'image/*',
            }),
            'introduction': forms.Textarea(attrs={
                'class': 'self-stretch h-[120px] rounded-lg border border-[#d88e30] px-4 py-2',
            }),
            'content': forms.Textarea(attrs={
                'class': 'self-stretch h-[700px] rounded-lg border border-[#d88e30] px-4 py-2',
            }),
        }
