from django.urls import path
from .views import register, login_view, logout_user

app_name = 'authentication'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),  # Use custom logout view
]
