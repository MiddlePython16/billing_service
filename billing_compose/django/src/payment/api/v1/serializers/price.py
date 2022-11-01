from payment.models import Price
from rest_framework import serializers
from payment.api.v1.utils import error_messages


class PriceToItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        exclude = ['item_id', 'id']


class MutationPriceSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        price = self.Meta.model.objects.filter(
            item_id=validated_data['item_id'],
            currency=validated_data['currency'],
        ).first()

        if price is not None:
            raise serializers.ValidationError(
                error_messages.ITEM_ALREADY_HAVE_PRICE_IN_THIS_CURRENCY,
            )

        return super().create(validated_data)

    class Meta:
        model = Price
        fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'
