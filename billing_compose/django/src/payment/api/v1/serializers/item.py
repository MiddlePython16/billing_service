from payment.api.v1.serializers.price import PriceSerializer
from payment.models import Item, Permission, Price
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all())
    item_prices = PriceSerializer(many=True)

    def create(self, validated_data):
        item_prices = validated_data.pop('item_prices')
        item = Item.objects.create(**validated_data)
        for price in item_prices:
            Price.objects.create(item_id=item, **price)

    class Meta:
        model = Item
        fields = '__all__'
