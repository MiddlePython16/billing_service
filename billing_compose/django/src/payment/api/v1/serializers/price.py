from rest_framework import serializers

from payment.models import Price


class PriceToItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        exclude = ['item_id', 'id']


class MutationPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'
