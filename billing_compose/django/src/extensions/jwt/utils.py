import time

import jwt
from config import settings


def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.JWT_PUBLIC_KEY,
            algorithms=['HS256'],
        )
    except jwt.exceptions.ExpiredSignatureError as error:
        decoded = jwt.decode(
            token,
            settings.JWT_PUBLIC_KEY,
            algorithms=['HS256'],
            options={'verify_signature': False},
        )
        time_now = int(time.time())
        if time_now - decoded['exp'] < settings.AUTH_TOKEN_EXPIRE_IN_SECONDS:
            return decoded
        raise error
