from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

def getUserOrCreate(email):
    if not User.objects.filter(username=email).exists():
        raw_password = get_random_string(30) # the user must reset the password to login (we dont care about this password)
        user = User.objects.create_user(email=email, username=email, password=raw_password)
    else:
        user = User.objects.get(username=email)

    return user