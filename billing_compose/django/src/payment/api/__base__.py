from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class FlexibleSerializerMixin:
    serializers = {}

    def get_serializer_key(self):
        return self.action

    def get_serializer_class(self):
        key = self.get_serializer_key()
        serializer_class = self.serializers.get(key, None) or self.serializer_class
        assert serializer_class is not None, (
            "'%s' should either enrich `.serializers` with '%s',"
            'or override the `get_serializer_class()` method or include serializer_class attribute'
            % self.__class__.__name__, key,
        )
        return serializer_class


class NestedPathLookupMixin:
    lookup_nested_fields = []
    lookup_nested_url_kwargs = []

    def get_nested_url_fields(self):
        self.lookup_nested_url_kwargs = self.lookup_nested_url_kwargs or \
                                        self.lookup_nested_fields
        return {field: self.kwargs[key] for field, key in zip(self.lookup_nested_fields,
                                                              self.lookup_nested_url_kwargs)}

    def get_queryset(self):
        return super().get_queryset().filter(**self.get_nested_url_fields())

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data | self.get_nested_url_fields())
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CLDModelViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    pass
