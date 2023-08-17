from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from django.utils import timezone
from CRM import settings


class TokenExpiredAuthentication(TokenAuthentication):
    def authenticate(self, request):
        try:
            user, token = super().authenticate(request=request)
        except TypeError:
            return None
        # if (timezone.now() - token.created).seconds > settings.TOKEN_TIME:
        #     token.delete()
        #     raise exceptions.AuthenticationFailed(f'{settings.TOKEN_TIME} seconds passed')
        return user, token
