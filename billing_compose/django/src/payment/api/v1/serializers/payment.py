from django.urls import reverse
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from config import settings
from payment.api.v1.serializers.item import ItemSerializer
from payment.models import Payment, Item, ItemsToPayments


class BasePaymentSerializer(serializers.ModelSerializer):
    pay_url = serializers.SerializerMethodField()
    variant = serializers.ChoiceField(settings.PAYMENT_VARIANTS)

    @extend_schema_field(serializers.CharField())
    def get_pay_url(self, obj):
        return f'{reverse("payment_details")}/{obj.id}'

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['pay_url',
                            'token',
                            'captured_amount',
                            'fraud_status',
                            'fraud_message',
                            'transaction_id',
                            'tax',
                            'status']


class MutationPaymentSerializer(BasePaymentSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, queryset=Item.objects.all())


class PaymentSerializer(BasePaymentSerializer):
    items = ItemSerializer(many=True)


class MutationItemsToPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemsToPayments
        exclude = ['id']
        optional_fields = ['payment_id']
