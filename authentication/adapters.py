from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.shortcuts import redirect


User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Automatically link Google login to an existing user if the email matches.
        """
        if sociallogin.user.email:
            try:
                existing_user = User.objects.get(email=sociallogin.user.email)
                sociallogin.connect(request, existing_user)
            except User.DoesNotExist:
                user = User.objects.create(
                    email=sociallogin.user.email,
                )
                user.set_unusable_password()
                user.save()
                sociallogin.connect(request, user)