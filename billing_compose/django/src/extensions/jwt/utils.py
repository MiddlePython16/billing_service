import time

import jwt

from config import settings


def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(token,
                          settings.JWT_PUBLIC_KEY,
                          algorithms=['HS256'])
    except jwt.exceptions.ExpiredSignatureError as e:
        decoded = jwt.decode(token,
                             settings.JWT_PUBLIC_KEY,
                             algorithms=['HS256'],
                             options={'verify_signature': False})
        time_now = int(time.time())
        if time_now - decoded['exp'] < 600:
            return decoded
        raise e
