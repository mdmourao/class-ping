from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model

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
                pass  # No existing user, let Allauth create a new one