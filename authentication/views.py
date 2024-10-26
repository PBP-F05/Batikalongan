from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from authentication.forms import CreateUser, UserForm
from django.contrib.auth.forms import AuthenticationForm
from authentication.models import User
from django.contrib import messages
from django.core import serializers
import datetime
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

# Register function
def register(request):
    form = CreateUser()
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')  # Redirect to login page after registration
        else:
            messages.error(request, 'Please correct the errors below.')
    return render(request, 'register.html', {'form': form})

# Login function
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("catalog"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    else:
        form = AuthenticationForm(request)
    return render(request, "login.html", {"form": form})
