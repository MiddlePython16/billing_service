from typing import Optional

from django.http import HttpRequest, HttpResponse
from extensions.jwt.responses import HttpResponseUNAUTHORIZED


def handle_cookies(request: HttpRequest) -> str:
    return request.COOKIES.get('access_token_cookie', '')


def handle_headers(request: HttpRequest) -> str:
    header = request.headers.get('Authorization', '').split(' ')
    return header[1] if len(header) > 1 else ''


def raw_decoded_jwt_user(decoded_jwt: dict) -> dict:
    return decoded_jwt


def handle_unauthorized(exception: Optional[Exception] = None) -> HttpResponse:
    return HttpResponseUNAUTHORIZED(str(exception))


token_handlers = {
    'cookies': handle_cookies,
    'headers': handle_headers,
}

user_handler = raw_decoded_jwt_user

unauthorized_handler = handle_unauthorized
