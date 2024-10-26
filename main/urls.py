# batikalongan/main/urls.py
from django.urls import path
from .views import main_landing_page

app_name = 'main'

urlpatterns = [
    path('', main_landing_page, name='main_landing_page'),
]
