from rest_framework import serializers

from payment.models import PricesToItems


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricesToItems
        fields = '__all__'
