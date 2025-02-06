# forms.py
from django import forms
from django.core.exceptions import ValidationError
import pyotp
from django.conf import settings

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