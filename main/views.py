# batikalongan/main/views.py
from django.shortcuts import render

def main_landing_page(request):
    return render(request, 'main.html')
