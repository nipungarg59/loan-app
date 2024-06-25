from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


from users.authentication.jwt_utils import decode_jwt_token
from users.models import User
from ..constants import JWT_COOKIE_KEY


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get(JWT_COOKIE_KEY)

        if not token:
            return None

        payload = decode_jwt_token(token)
        if payload is None:
            raise AuthenticationFailed('Invalid or expired token')

        user = User.objects.get(id=payload['user_id'])
        setattr(user, "is_authenticated", True)
        return user, None
