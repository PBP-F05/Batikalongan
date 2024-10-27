from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.urls import reverse
from .forms import CreateUser, LoginForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateUser
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User

def register(request):
    form = CreateUser()
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('authentication:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    return render(request, 'register.html', {'form': form})

def login_view(request):
    form = LoginForm()
    UserModel = get_user_model()
    admin_username = "admin"
    admin_password = "adminpassword"

    # Cek apakah akun admin sudah ada
    if not UserModel.objects.filter(username=admin_username).exists():
        # Buat akun admin baru jika belum ada
        UserModel.objects.create_user(username=admin_username, password=admin_password)

    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Periksa kredensial admin
            if user.username == admin_username and user.check_password(admin_password):
                # Set variabel session untuk menandakan user adalah admin
                request.session['is_admin'] = True
                return redirect(reverse("main:main_landing_page"))  # Redirect ke dashboard admin
            return redirect(reverse("main:main_landing_page"))  # Redirect ke halaman utama setelah login
        else:
            messages.error(request, "Invalid credentials, please try again.")
    return render(request, "login.html", {"form": form})


def logout_user(request):
    logout(request)  # Logs out the user
    response = HttpResponseRedirect(reverse('main:main_landing_page'))  # Redirect to landing page after logout
    response.delete_cookie('last_login')  # Remove 'last_login' cookie
    return response