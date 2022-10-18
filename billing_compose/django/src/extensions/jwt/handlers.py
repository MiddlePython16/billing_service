from django.http import HttpRequest, HttpResponse

from extensions.jwt.responses import HttpResponsesUNAUTHORIZED


def handle_cookies(request: HttpRequest) -> str:
    return request.COOKIES.get('access_token_cookie', '')


def handle_headers(request: HttpRequest) -> str:
    header = request.headers.get('Authorization', '').split(' ')
    if len(header) > 1:
        return header[1]
    return ''


def raw_decoded_jwt_user(decoded_jwt: dict) -> dict:
    return decoded_jwt


def handle_unathorized(content: str = '') -> HttpResponse:
    return HttpResponsesUNAUTHORIZED(content)


token_handlers = {
    'cookies': handle_cookies,
    'headers': handle_headers,
}

user_handler = raw_decoded_jwt_user

unathorized_handler = handle_unathorized
