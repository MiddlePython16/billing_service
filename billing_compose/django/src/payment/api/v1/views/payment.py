from payment.api.v1.serializers.payment import MutationPaymentSerializer
from payment.models import Payment
from rest_framework import generics
from payment.api.v1.views.__base__ import CustomPaginator


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = MutationPaymentSerializer
    queryset = Payment.objects.all()


class PaymentListView(generics.ListAPIView):
    serializer_class = MutationPaymentSerializer
    queryset = Payment.objects.all()
    pagination_class = CustomPaginator


class PaymentRetrieve(generics.RetrieveAPIView):
    serializer_class = MutationPaymentSerializer
    queryset = Payment.objects.all()


class PaymentUpdateView(generics.UpdateAPIView):
    serializer_class = MutationPaymentSerializer
    queryset = Payment.objects.all()


class PaymentDestroyView(generics.DestroyAPIView):
    serializer_class = MutationPaymentSerializer
    queryset = Payment.objects.all()
