from payment.api.v1.serializers.permission import MutationPermissionSerializer
from payment.api.v1.serializers.price import PriceToItemSerializer
from payment.models import Item, Permission, PermissionsToItems, Price
from rest_framework import serializers


class MutationItemSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all())
    prices = PriceToItemSerializer(many=True, required=False)

    def create(self, validated_data):
        prices = validated_data.pop('prices')
        item = super().create(validated_data)
        for price in prices:
            Price.objects.create(item_id=item, **price)
        return item

    def update(self, instance, validated_data):
        prices = validated_data.pop('prices')
        for price in prices:
            obj = instance.prices.filter(currency=price['currency']).first()
            if obj is None:
                Price.objects.create(item_id=instance, **price)
                continue
            obj.value = price['value']
            obj.save()
        return super().update(instance, validated_data)

    def validate_prices(self, items):
        if len(items) != len({item['currency'] for item in items}):
            raise serializers.ValidationError('Prices must be unique')
        return items

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

    def create(self, validated_data):
        if self.Meta.model.objects.filter(item_id=validated_data['item_id'],
                                          user_id=validated_data['permission_id']).first() is not None:
            raise serializers.ValidationError('Item already have this permission')

        return super().create(validated_data)

    class Meta:
        model = PermissionsToItems
        exclude = ['id']
        optional_fields = ['item_id']
