from django.urls import path
from .views import register, login_view, logout_user, api_login, api_register

app_name = 'authentication'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('api/login/', api_login, name='api_login'), # Untuk flutter
    path('api/register/', api_register, name='api_register'),  # Untuk Flutter
]
    