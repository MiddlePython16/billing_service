import time

import jwt
from config import settings

EXPIRE_TIME_IN_SECONDS = 600


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
        if time_now - decoded['exp'] < EXPIRE_TIME_IN_SECONDS:
            return decoded
        raise error
