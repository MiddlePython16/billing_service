from payment.api.__base__ import (CLDModelViewSet, FlexibleSerializerMixin,
                                  NestedPathLookupMixin)
from payment.api.v1.serializers.item import (
    ItemSerializer, MutationItemSerializer,
    MutationPermissionsToItemsSerializer)
from payment.api.v1.views.__base__ import CustomPaginator
from payment.models import Item, PermissionsToItems
from rest_framework.viewsets import ModelViewSet


class ItemViewSet(FlexibleSerializerMixin, ModelViewSet):
    serializers = {
        'create': MutationItemSerializer,
        'list': ItemSerializer,
        'retrieve': ItemSerializer,
        'update': MutationItemSerializer,
        'partial_update': MutationItemSerializer,
        'destroy': ItemSerializer,
    }
    queryset = Item.objects.all()
    pagination_class = CustomPaginator


class PermissionToItemViewSet(FlexibleSerializerMixin, NestedPathLookupMixin, CLDModelViewSet):
    serializers = {
        'create': MutationPermissionsToItemsSerializer,
        'list': MutationPermissionsToItemsSerializer,
        'destroy': MutationPermissionsToItemsSerializer,
    }
    queryset = PermissionsToItems.objects.all()

    lookup_field = 'permission_id'
    lookup_url_kwarg = 'id'

    lookup_nested_fields = ['item_id']
    lookup_nested_url_kwargs = ['item_pk']
