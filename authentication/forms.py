from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['nama', 'username', 'password1', 'password2']  # Remove 'role'
    widgets = {
        'nama': forms.TextInput(attrs={'class': 'w-full h-12 px-4 border border-[#d88e30] rounded-lg'}),
        'username': forms.TextInput(attrs={'class': 'w-full h-12 px-4 border border-[#d88e30] rounded-lg'}),
        'password1': forms.PasswordInput(attrs={'class': 'w-full h-12 px-4 border border-[#d88e30] rounded-lg'}),
        'password2': forms.PasswordInput(attrs={'class': 'w-full h-12 px-4 border border-[#d88e30] rounded-lg'}),
    }



class LoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full h-12 px-4 border border-[#d88e30] rounded-lg focus:outline-none focus:border-[#bf7428]'}),
            'password': forms.PasswordInput(attrs={'class': 'w-full h-12 px-4 border border-[#d88e30] rounded-lg focus:outline-none focus:border-[#bf7428]'}),
        }
