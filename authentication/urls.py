from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = "authentication"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("reset_password/", auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password sent/', auth_views.PasswordResetDoneView.as_view(),name= 'password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name= 'password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view() , name= 'password_reset_complete'),
]
