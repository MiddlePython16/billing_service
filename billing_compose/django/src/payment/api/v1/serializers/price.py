from rest_framework import serializers

from payment.models import Price


class PriceToItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        exclude = ['item_id', 'id']


class MutationPriceSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        if self.Meta.model.objects.filter(item_id=validated_data['item_id'],
                                          currency=validated_data['currency']).first() is not None:
            raise serializers.ValidationError('Item already have price in this currency')

        return super().create(validated_data)

    class Meta:
        model = Price
        fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'
