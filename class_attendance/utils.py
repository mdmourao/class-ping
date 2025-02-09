from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model 


def getUserOrCreate(email):
    UserModel = get_user_model()
    if not UserModel.objects.filter(email=email).exists():
        raw_password = get_random_string(30) # the user must reset the password to login (we dont care about this password)
        user = UserModel.objects.create_user(email=email, password=raw_password)
    else:
        user = UserModel.objects.get(email=email)

    return user