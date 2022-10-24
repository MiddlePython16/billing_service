from rest_framework import serializers

from payment.models import Item
from payment.api.v1.serializers.price import PriceSerializer


class ItemSerializer(serializers.ModelSerializer):
    prices = PriceSerializer(many=True, required=False)

    class Meta:
        model = Item
        fields = '__all__'
