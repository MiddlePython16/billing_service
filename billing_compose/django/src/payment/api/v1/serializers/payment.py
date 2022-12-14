from urllib.parse import urljoin

from config import settings
from django.urls import reverse
from drf_spectacular.utils import extend_schema_field
from payment.api.v1.serializers.item import ItemSerializer
from payment.models import Item, ItemsToPayments, Payment
from payments.core import get_base_url
from rest_framework import serializers
from payment.api.v1.utils import error_messages


class BasePaymentSerializer(serializers.ModelSerializer):
    pay_url = serializers.SerializerMethodField()
    variant = serializers.ChoiceField(settings.PAYMENT_VARIANTS)

    @extend_schema_field(serializers.CharField())
    def get_pay_url(self, obj):
        return urljoin(get_base_url(), reverse('payment_details', obj.id))

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

    def create(self, validated_data):
        if self.Meta.model.objects.filter(item_id=validated_data['item_id'],
                                          user_id=validated_data['payment_id']).first() is not None:
            raise serializers.ValidationError(error_messages.PAYMENT_ALREADY_HAVE_THIS_ITEM)

        return super().create(validated_data)

    class Meta:
        model = ItemsToPayments
        exclude = ['id']
        optional_fields = ['payment_id']
