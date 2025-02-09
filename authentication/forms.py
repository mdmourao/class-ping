from django import forms   
from django.contrib.auth import get_user_model 

class RegisterForm(forms.ModelForm):
  class Meta:
    model = get_user_model()  
    fields = [ "first_name", "last_name", "email", "password"]

    widgets = {
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