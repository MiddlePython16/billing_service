from rest_framework.viewsets import ModelViewSet

from payment.api.__base__ import FlexibleSerializerMixin, NestedPathLookupMixin, CLDModelViewSet
from payment.api.v1.serializers.payment import MutationPaymentSerializer, MutationItemsToPaymentsSerializer
from payment.api.v1.views.__base__ import CustomPaginator
from payment.models import Payment, ItemsToPayments


class PaymentViewSet(FlexibleSerializerMixin, ModelViewSet):
    serializers = {
        'create': MutationPaymentSerializer,
        'list': MutationPaymentSerializer,
        'retrieve': MutationPaymentSerializer,
        'update': MutationPaymentSerializer,
        'partial_update': MutationPaymentSerializer,
        'destroy': MutationPaymentSerializer,
    }
    queryset = Payment.objects.all()
    pagination_class = CustomPaginator


class ItemToPaymentViewSet(FlexibleSerializerMixin, NestedPathLookupMixin, CLDModelViewSet):
    serializers = {
        'create': MutationItemsToPaymentsSerializer,
        'list': MutationItemsToPaymentsSerializer,
        'destroy': MutationItemsToPaymentsSerializer,
    }
    queryset = ItemsToPayments.objects.all()

    lookup_field = 'item_id'
    lookup_url_kwarg = 'id'

    lookup_nested_fields = ['payment_id']
    lookup_nested_url_kwargs = ['payment_pk']
