from django.shortcuts import render, redirect
from .forms import UserRegForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, f"You are already logged in as {request.user.username}")
        return HttpResponseRedirect(reverse("orders:index"))
    else:
        if request.method == "POST":
            user_form = UserRegForm(data=request.POST)
            if user_form.is_valid():
                user = user_form.save()
                user.set_password(user_form.cleaned_data.get("password"))
                user.save()
                username = user_form.cleaned_data.get("username")
                raw_password = user_form.cleaned_data.get("password")
                userlog = authenticate(username=username, password=raw_password)
                login(request, userlog)
                messages.success(request, f"{user.first_name}, you registered successfully!")
                return HttpResponseRedirect(reverse("orders:index"))
            else:
                messages.warning(request, "Invalid credentials.Please check it out.")
                return render(request, "user/register.html", {"form": user_form})
        else:
            messages.info(request, "Welcome to pizza. Register here to get started.")
            return render(request, "user/register.html", {"form": UserRegForm()})


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, f"You are already logged in as {request.user.username}")
        return HttpResponseRedirect(reverse("orders:index"))
    else:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"{user.first_name}, you logged in successfully!")
                return HttpResponseRedirect(reverse("orders:index"))
            else:
                messages.warning(request, "Invalid credentials.")
                return render(request, "user/login.html")
        else:
            messages.info(request,"Login here!")
            return render(request, "user/login.html")


@login_required(login_url='user:register')
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return HttpResponseRedirect(reverse("user:login"))