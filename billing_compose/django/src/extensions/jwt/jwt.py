from functools import wraps
from typing import Optional

from config import settings
from django.http import HttpRequest
from extensions.jwt.exceptions import NoRequestInstanceError
from extensions.jwt.handlers import (token_handlers, unauthorized_handler,
                                     user_handler)
from extensions.jwt.utils import decode_jwt
from jwt import PyJWTError


def get_request(*args, **kwargs):
    for item in args:  # noqa: WPS110
        if isinstance(item, HttpRequest):
            return item
    raise NoRequestInstanceError('No request instance')


def jwt_required(optional: bool = False):  # noqa: WPS231
    """
    Wrap your view function in it,
    and you will get current_user as a named argument of your view function.
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            current_user = None

            request = get_request(*args, **kwargs)
            token = get_jwt_token(request=request)

            if token is None and not optional:
                return unauthorized_handler()

            if token:
                try:
                    token = decode_jwt(token=token)
                    current_user = user_handler(decoded_jwt=token)
                except PyJWTError as error:
                    return unauthorized_handler(error_content=str(error))

            return func(*args, **(kwargs | {'current_user': current_user}))

        return inner

    return func_wrapper


def get_jwt_token(request) -> Optional[str]:
    for item in settings.JWT_TOKEN_LOCATION:  # noqa: WPS110
        request_handler = token_handlers.get(item, None)
        if request_handler is None:
            continue

        token = request_handler(request)
        if token:
            return token
