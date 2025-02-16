# forms.py
from django import forms
from django.core.exceptions import ValidationError
import pyotp
from django.conf import settings
from .models import *

class StudentNumberForm(forms.Form):
    student_number = forms.IntegerField(label="Número De Aluno", min_value=1, required=True, widget=forms.NumberInput(
            attrs={
                "class": "form-control form-control-lg mt-2",
                "placeholder": "21805495",
            }
        ))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

class NameForm(forms.Form):
    first_name = forms.CharField(label="Primeiro Nome", max_length=15, required=True, widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg mt-2",
                "placeholder": "Lara",
            }
        ))
    
    last_name = forms.CharField(label="Último Nome", max_length=15,required=True, widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg mt-2",
                "placeholder": "Silva",
            }
        ))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

class CodeForm(forms.Form):
    code = forms.IntegerField(label="Código", min_value=1, max_value=999999, required=True, widget=forms.NumberInput(
            attrs={
                "class": "form-control form-control-lg mt-2",
                "placeholder": "123456",
            }
        ))

    def __init__(self, *args, **kwargs):
        # Expect the session to be passed via form kwargs
        self.session = kwargs.pop('session', None)
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if self.session:
            totp = pyotp.TOTP(str(self.session.secret), interval=settings.OTP_INTERVAL)
            if not totp.verify(code):
                raise ValidationError("Código Inválido")
        return code
    
class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ["label", "image"]

        widgets = {
            "label": forms.TextInput(attrs={
                        "class": "form-control form-control-lg",
                        "placeholder": "Universidade de Lisboa",
                    }),
            
            "image": forms.FileInput(attrs={
                        "class": "form-control form-control-lg",
                    }),
            
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

class AddEmailForm(forms.Form):
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-lg mt-2",
                "placeholder": "example@example.com",
            }
        ))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["label"]

        widgets = {
            "label": forms.TextInput(attrs={
                        "class": "form-control form-control-lg",
                        "placeholder": "Web Development",
                    }),
            
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""


class SchoolClassForm(forms.ModelForm):
    email_professor = forms.EmailField(
            label="Email Professor",
            required=True,
            widget=forms.EmailInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "professor@example.com",
                }
            )
        )


    class Meta:
        model = SchoolClass
        fields = ["label","class_id", "weekday" ,"start_time", "end_time", "year", "semester"]

        widgets = {
            "label": forms.TextInput(attrs={
                        "class": "form-control form-control-lg",
                        "placeholder": "Web Development",
                    }),

            "weekday": forms.Select(attrs={
                        "class": "form-control form-control-lg",
                        
                    }),

            "class_id": forms.TextInput(attrs={
                        "class": "form-control form-control-lg",
                        "placeholder": "LD01EINF02",
                    }),
            "start_time": forms.TimeInput(attrs={
                        "class": "form-control form-control-lg",
                        "placeholder": "08:00",
                        "type": "time" 
                    }),
            "end_time": forms.TimeInput(attrs={
                        "class": "form-control form-control-lg",
                        "placeholder": "10:00",
                         "type": "time" 
                    }),
            "year": forms.NumberInput(attrs={
                        "class": "form-control form-control-lg",
                        "placeholder": "2021",
                    }),
            "semester": forms.NumberInput(attrs={
                        "class": "form-control form-control-lg",
                        "placeholder": "1",
                    }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

        
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        if start_time and end_time and start_time >= end_time:
            self.add_error("start_time", "Start time must be before end time")
        return cleaned_data