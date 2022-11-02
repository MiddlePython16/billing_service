from payment.api.__base__ import (CLDModelViewSet, FlexibleSerializerMixin,
                                  NestedPathLookupMixin)
from payment.api.v1.serializers.user import (MutationItemsToUsersSerializer,
                                             MutationUserSerializer,
                                             UserSerializer)
from payment.api.v1.views.__base__ import CustomPaginator
from payment.models import ItemsToUsers, User
from rest_framework.viewsets import ModelViewSet


class UserViewSet(FlexibleSerializerMixin,
                  ModelViewSet):
    serializers = {
        'create': MutationUserSerializer,
        'list': UserSerializer,
        'retrieve': UserSerializer,
        'update': MutationUserSerializer,
        'partial_update': MutationUserSerializer,
        'destroy': UserSerializer,
    }
    queryset = User.objects.all()
    pagination_class = CustomPaginator


class ItemToUserViewSet(FlexibleSerializerMixin, NestedPathLookupMixin, CLDModelViewSet):
    serializers = {
        'create': MutationItemsToUsersSerializer,
        'list': MutationItemsToUsersSerializer,
        'destroy': MutationItemsToUsersSerializer,
    }
    queryset = ItemsToUsers.objects.all()

    lookup_field = 'item_id'
    lookup_url_kwarg = 'id'

    lookup_nested_fields = ['user_id']
    lookup_nested_url_kwargs = ['user_pk']
