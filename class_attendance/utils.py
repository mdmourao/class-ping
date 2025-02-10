from django.conf import settings
from django.contrib.auth import get_user_model 

def getUserOrCreate(email):
    UserModel = get_user_model()
    if not UserModel.objects.filter(email=email).exists():
        user = UserModel.objects.create(email=email)
        user.set_unusable_password()
        user.save()
    else:
        user = UserModel.objects.get(email=email)

    return user