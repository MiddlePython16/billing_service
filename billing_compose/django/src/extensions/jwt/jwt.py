from functools import wraps

from django.http import HttpRequest
from jwt import PyJWTError

from config import settings
from extensions.jwt.exceptions import NoRequestInstance
from extensions.jwt.handlers import user_handler, token_handlers, unathorized_handler
from extensions.jwt.utils import decode_jwt


def get_request(*args, **kwargs):
    for item in args:
        if isinstance(item, HttpRequest):
            return item
    raise NoRequestInstance('No request instance')


def jwt_required(optional: bool = False):
    """
    Wrap your view function in it and you'l get current_user as a named argument of your view function


    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            current_user = None

            request = get_request(*args, **kwargs)
            token = ''
            for item in settings.JWT_TOKEN_LOCATION:
                handler = token_handlers.get(item, None)
                if handler is None:
                    continue

                token = handler(request)
                if token:
                    break

            if not token and not optional:
                return unathorized_handler()
            elif token:
                try:
                    token = decode_jwt(token=token)
                    current_user = user_handler(decoded_jwt=token)
                except PyJWTError as e:
                    return unathorized_handler(content=str(e))

            return func(*args, **(kwargs | {'current_user': current_user}))

        return inner

    return func_wrapper
