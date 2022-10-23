from rest_framework import generics

from payment.api.v1.serializers.payment import MutationPaymentSerializer
from payment.models import Payment


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = MutationPaymentSerializer
    queryset = Payment.objects.all()
