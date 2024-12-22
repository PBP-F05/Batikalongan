import json
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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
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


@csrf_exempt
def api_login(request):
    admin_username = "admin"
    admin_password = "adminpassword"

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({
                "status": False,
                "message": "Username dan password wajib diisi."
            }, status=400)

        # Periksa apakah kredensial admin cocok
        if username == admin_username and password == admin_password:
            user = authenticate(username=admin_username, password=admin_password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    request.session['is_admin'] = True
                    return JsonResponse({
                        "status": True,
                        "message": "Login sukses! Anda masuk sebagai admin.",
                        "username": user.username,
                        "is_admin": True,  # Tandai sebagai admin
                    }, status=200)
                else:
                    return JsonResponse({
                        "status": False,
                        "message": "Akun admin dinonaktifkan."
                    }, status=403)
            else:
                return JsonResponse({
                    "status": False,
                    "message": "Akun admin belum terdaftar di sistem."
                }, status=401)

        # Validasi login untuk user biasa
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return JsonResponse({
                    "status": True,
                    "message": "Login sukses!",
                    "username": user.username,
                    "is_admin": user.is_staff,  # Informasi admin tetap disertakan
                }, status=200)
            else:
                return JsonResponse({
                    "status": False,
                    "message": "Akun Anda dinonaktifkan."
                }, status=403)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal. Username atau password salah."
            }, status=401)
    else:
        return JsonResponse({
            "status": False,
            "message": "Metode HTTP tidak valid."
        }, status=405)


# Flutter
@csrf_exempt
def api_register(request):
    """
    API endpoint for user registration, compatible with Flutter.
    """
    User = get_user_model()
    if request.method == 'POST':
        data = json.loads(request.body)
        nama = data['nama']
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
        
        # Create the new user
        user = User.objects.create_user(nama=nama, username=username, password=password1)
        user.save()
        
        return JsonResponse({
            "nama": user.nama,
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

@csrf_exempt
def api_logout(request):
    username = request.user.username

    try:
        logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)

# Flutter
@csrf_exempt
def admin_login(request):
    admin_username = "admin"
    admin_password = "adminpassword"
    UserModel = get_user_model()

    # Buat akun admin jika belum ada
    if not UserModel.objects.filter(username=admin_username).exists():
        UserModel.objects.create_user(username=admin_username, password=admin_password)

    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                is_admin = (user.username == admin_username and user.check_password(admin_password))
                return JsonResponse({
                    "status": True,
                    "message": "Login successful!",
                    "username": user.username,
                    "is_admin": is_admin,  # Informasi apakah user adalah admin
                }, status=200)
            else:
                return JsonResponse({
                    "status": False,
                    "message": "Account is deactivated."
                }, status=403)
        else:
            return JsonResponse({
                "status": False,
                "message": "Invalid credentials. Please try again."
            }, status=401)
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)