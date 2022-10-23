from django.urls import reverse
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from config import settings
from payment.models import Payment


class MutationPaymentSerializer(serializers.ModelSerializer):
    pay_url = serializers.SerializerMethodField()
    variant = serializers.ChoiceField(settings.PAYMENT_VARIANTS)
    currency = serializers.ChoiceField(settings.PAYMENT_CURRENCIES)

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
