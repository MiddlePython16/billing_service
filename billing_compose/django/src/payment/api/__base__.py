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
            "or override the `get_serializer_class()` method or include serializer_class attribute"
            % self.__class__.__name__, key
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

# class FlexibleQuerysetMixin:
#     querysets = {}
#
#     def get_queryset_key(self):
#         return self.action
#
#     def get_queryset(self):
#         key = self.get_queryset_key()
#         queryset = self.querysets.get(key, None)
#         queryset = queryset if queryset is not None else self.queryset
#         assert queryset is not None, (
#             "'%s' should either enrich `.querysets` with '%s',"
#             "or override the `get_queryset()` method or include queryset attribute"
#             % self.__class__.__name__, key
#         )
#
#         if isinstance(queryset, QuerySet):
#             # Ensure queryset is re-evaluated on each request.
#             queryset = queryset.all()
#         return queryset


# class MultipleLookupFieldsMixin:
#     lookup_fields = ['pk']
#     lookup_url_kwargs = []
#
#     def get_object(self):
#         """
#         Returns the object the view is displaying.
#
#         You may want to override this if you need to provide non-standard
#         queryset lookups.  Eg if objects are referenced using multiple
#         keyword arguments in the url conf.
#         """
#         queryset = self.filter_queryset(self.get_queryset())
#
#         # Perform the lookup filtering.
#         if not self.lookup_url_kwargs:
#             self.lookup_url_kwargs = self.lookup_fields
#
#         assert self.lookup_url_kwargs in self.kwargs, (
#                 'Expected view %s to be called with a URL keywords arguments '
#                 'named "%s". Fix your URL conf, or set the `.lookup_fields` '
#                 'attributes on the view correctly.' %
#                 (self.__class__.__name__, self.lookup_url_kwargs)
#         )
#
#         filter_kwargs = {field: self.kwargs[key] for field, key in zip(self.lookup_fields, self.lookup_url_kwargs)}
#         obj = get_object_or_404(queryset, **filter_kwargs)
#
#         # May raise a permission denied
#         self.check_object_permissions(self.request, obj)
#
#         return obj
