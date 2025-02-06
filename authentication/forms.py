from django import forms    # formulários Django
from django.contrib.auth.models import User   

class RegisterForm(forms.ModelForm):
  class Meta:
    model = User        
    fields = ["username", "first_name", "last_name", "email", "password"]

    widgets = {
      "username": forms.TextInput(attrs={
                "class": "form-control form-control-lg",
                "placeholder": "supermegausername",
            }),
      "first_name": forms.TextInput(attrs={
                "class": "form-control form-control-lg mt-2",
                "placeholder": "Lara",
            }),
      "last_name": forms.TextInput(attrs={
                "class": "form-control form-control-lg mt-2",
                "placeholder": "Silva",
            }),
      "password": forms.PasswordInput(attrs={
                "class": "form-control form-control-lg mt-2",
                
            }),
      "email": forms.EmailInput(attrs={
                "class": "form-control form-control-lg mt-2",
                "placeholder": "example@example.com",
            })
    }   