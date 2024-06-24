from datetime import datetime

import jwt
from django.conf import settings


def generate_jwt_token(user):
    expiration = datetime.now() + settings.JWT_EXPIRATION_DELTA
    payload = {
        'user_id': user.id,
        'exp': expiration,
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token


def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
