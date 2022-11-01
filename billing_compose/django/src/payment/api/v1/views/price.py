from payment.api.__base__ import FlexibleSerializerMixin
from payment.api.v1.serializers.price import (MutationPriceSerializer,
                                              PriceSerializer)
from payment.api.v1.views.__base__ import CustomPaginator
from payment.models import Price
from rest_framework.viewsets import ModelViewSet


class PriceViewSet(FlexibleSerializerMixin, ModelViewSet):
    serializers = {
        'create': MutationPriceSerializer,
        'list': PriceSerializer,
        'retrieve': PriceSerializer,
        'update': MutationPriceSerializer,
        'partial_update': MutationPriceSerializer,
        'destroy': PriceSerializer,
    }
    queryset = Price.objects.all()
    pagination_class = CustomPaginator
