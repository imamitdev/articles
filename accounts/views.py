from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login as auth_user
from django.contrib.auth.decorators import login_required


# Create your views here.
def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            auth_user(request, user)
            messages.success(request, "User successfully Logged in")
            return redirect("/")
        else:
            messages.error(request, "Invalid User")
            return redirect("login")

    return render(request, "account/login.html")


def registration(request):
    if request.method == "POST":
        full_name = request.POST["full_name"]
        email = request.POST["email"]
        number = request.POST["mobile_no"]
        password = request.POST["password"]
        cpassword = request.POST["confirm_password"]
        user_check = User.objects.filter(username=email).exists()
        print(user_check)
        if len(number) != 10:
            messages.error(request, "Number Should be 10 digit")
            return redirect("/account/registration")
        elif password != cpassword:
            messages.error(
                request, "Password and confirm password did't Match "
            )
            return redirect("/account/registration/")
        elif user_check == True:
            messages.error(request, "User Already exist .")
            return redirect("/account/registration/")
        else:
            user = User.objects.create_user(
                email=email, username=email, password=password
            )
            user.first_name = full_name
            user.save()
            messages.success(request, "Member successfully register ")
            return redirect("/account/login/")

    return render(request, "account/registration.html")


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request, "You are Logged out")
    return redirect("/account/login/")
