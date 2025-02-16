from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import RegisterForm

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            email=request.POST["email"],
            password=request.POST["password"]
        )
        if user:
            login(request, user)
            return redirect("/class_attendance/universities")
        else:
            context = {
                "error": "Invalid!",
            }
            return render(request, "authentication/login.html", context)
    
    return render(request, "authentication/login.html")

def logout_view(request):
    logout(request)
    return redirect("/authentication/login")