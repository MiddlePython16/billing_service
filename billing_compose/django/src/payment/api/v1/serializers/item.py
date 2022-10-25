from rest_framework import serializers

from payment.api.v1.serializers.permission import MutationPermissionSerializer
from payment.api.v1.serializers.price import PriceToItemSerializer
from payment.models import Item, Permission, Price, PermissionsToItems


class MutationItemSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all())
    prices = PriceToItemSerializer(many=True, required=False)

    def create(self, validated_data):
        prices = validated_data.pop('prices')
        item = super().create(validated_data)
        for price in prices:
            Price.objects.create(item_id=item, **price)
        return item

    class Meta:
        model = Item
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    permissions = MutationPermissionSerializer(many=True)
    prices = PriceToItemSerializer(many=True)

    class Meta:
        model = Item
        fields = '__all__'


class MutationPermissionsToItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionsToItems
        exclude = ['id']
        optional_fields = ['item_id']
