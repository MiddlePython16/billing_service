from http import HTTPStatus

from django.http import HttpResponse


class HttpResponsesUNAUTHORIZED(HttpResponse):
    status_code = HTTPStatus.UNAUTHORIZED