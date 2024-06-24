from django.contrib.auth.backends import BaseBackend

from users.authentication.jwt_utils import decode_jwt_token
from users.models import User
from ..constants import JWT_COOKIE_KEY


class JWTAuthenticationBackend(BaseBackend):
    def authenticate(self, request, token=None):
        if token is None:
            token = request.COOKIES.get(JWT_COOKIE_KEY)
        if token is None:
            return None

        payload = decode_jwt_token(token)
        if payload is None:
            return None

        try:
            user = User.objects.get(id=payload['user_id'])
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
