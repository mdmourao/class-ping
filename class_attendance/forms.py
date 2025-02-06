# forms.py
from django import forms
from django.core.exceptions import ValidationError
import pyotp
from django.conf import settings

class StudentNumberForm(forms.Form):
    student_number = forms.IntegerField(label="Número De Aluno", min_value=1, required=True)

class NameForm(forms.Form):
    first_name = forms.CharField(label="Primeiro Nome", max_length=15, required=True)
    last_name = forms.CharField(label="Último Nome", max_length=15,required=True)

class CodeForm(forms.Form):
    code = forms.IntegerField(label="Código", min_value=1, max_value=999999, required=True)

    def __init__(self, *args, **kwargs):
        # Expect the session to be passed via form kwargs
        self.session = kwargs.pop('session', None)
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if self.session:
            totp = pyotp.TOTP(str(self.session.secret), interval=settings.OTP_INTERVAL)
            if not totp.verify(code):
                raise ValidationError("Código Inválido")
        return code