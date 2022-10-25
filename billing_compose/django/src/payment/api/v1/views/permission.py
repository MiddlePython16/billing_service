from rest_framework.viewsets import ModelViewSet

from payment.api.__base__ import FlexibleSerializerMixin
from payment.api.v1.serializers.permission import PermissionSerializer, MutationPermissionSerializer
from payment.api.v1.views.__base__ import CustomPaginator
from payment.models import Permission


class PermissionViewSet(FlexibleSerializerMixin, ModelViewSet):
    serializers = {
        'create': MutationPermissionSerializer,
        'list': PermissionSerializer,
        'retrieve': PermissionSerializer,
        'update': MutationPermissionSerializer,
        'partial_update': MutationPermissionSerializer,
        'destroy': PermissionSerializer,
    }
    queryset = Permission.objects.all()
    pagination_class = CustomPaginator
