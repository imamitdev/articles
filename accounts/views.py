from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from .forms import UserCreateForm, UserLoginForm


# Create your views here.
def registration(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in the user after registration
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                # Redirect to a success page or homepage
                return redirect("home")
    else:
        form = UserCreateForm()

    return render(request, "account/registration.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                # Redirect to a success page or homepage
                return redirect("home")
    else:
        form = UserLoginForm()

    return render(request, "account/login.html", {"form": form})


def logout(request):
    auth.logout(request)
    messages.success(request, "You are Logged out")
    return redirect("/account/login/")
