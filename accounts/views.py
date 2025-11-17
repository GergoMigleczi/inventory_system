from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form, "hide_nav": True})

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")   # change later
        else:
            error = "Invalid credentials"
            return render(request, "accounts/login.html", {"error": error, "hide_nav": True})

    return render(request, "accounts/login.html", {"hide_nav": True})