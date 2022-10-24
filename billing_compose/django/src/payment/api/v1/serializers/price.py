from payment.models import Price
from rest_framework import serializers


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'
