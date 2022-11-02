from http import HTTPStatus

from django.http import HttpResponse


class HttpResponseUNAUTHORIZED(HttpResponse):
    status_code = HTTPStatus.UNAUTHORIZED
