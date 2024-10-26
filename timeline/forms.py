from django.forms import ModelForm
from django import forms
from .models import *

class PostCreateForm(ModelForm):
   class Meta:
      model = Post
      fields = ['files', 'body']
      labels = {
         'body' : 'Caption',
      }
      widgets = {
         'body' : forms.Textarea(attrs={'rows': 3, 'class': 'font5 text-4xl'}),
         'url' : forms.TextInput(attrs={'placeholder': 'Add urls ...'}),
      }

class PostEditForm(ModelForm):
   class Meta:
      model = Post
      fields = ['body',]
      labels = {
         'body' : '',
      }
      widgets = {
         'body' : forms.Textarea(attrs={'rows': 3, 'class': 'font5 text-4xl'}),
      }

class CommentCreateForm(ModelForm):
   class Meta:
      model = Comment
      fields = ['body',]
      labels = {
         'body' : '',
      }
      widgets = {
         'body' : forms.TextInput(attrs={
            'placeholder': 'Add Comment ...',
            'style': 'resize:none;',
            'class': 'font-semibold text-lg w-full p-4 border rounded-lg shadow-md',
         })
      }

class ReplyCreateForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder': 'Add reply ...', 'class': "!text-sm"})
        }
        labels = {
            'body': ''
        }