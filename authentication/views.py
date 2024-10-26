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
from django.http import HttpResponseRedirect
from django.urls import reverse

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
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect(reverse("main:main_landing_page"))  # Redirect to main landing page after login
        else:
            messages.error(request, "Invalid credentials, please try again.")
    return render(request, "login.html", {"form": form})

def logout_user(request):
    logout(request)  # Logs out the user
    response = HttpResponseRedirect(reverse('main:main_landing_page'))  # Redirect to landing page after logout
    response.delete_cookie('last_login')  # Remove 'last_login' cookie
    return response