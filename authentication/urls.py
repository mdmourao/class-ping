from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = "authentication"

urlpatterns = [
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
]
