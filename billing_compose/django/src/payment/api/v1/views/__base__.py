from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination


class CustomPaginator(PageNumberPagination):
    page_size = 10
