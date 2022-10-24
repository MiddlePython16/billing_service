from payment.models import Price
from rest_framework import serializers


class MutationPriceSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Price.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.currency = validated_data.get('currency', instance.currency)
        instance.value = validated_data.get('value', instance.value)
        instance.save()
        return instance

    class Meta:
        model = Price
        fields = '__all__'
        exclude = ['item_id']


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'
