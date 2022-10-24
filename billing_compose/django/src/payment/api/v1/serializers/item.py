from payment.api.v1.serializers.price import MutationPriceSerializer
from payment.api.v1.serializers.permission import MutationPermissionSerializer
from payment.models import Item, Permission, Price
from rest_framework import serializers


class MutationItemSerializer(serializers.ModelSerializer):
    permissions = MutationPermissionSerializer(many=True)
    item_prices = MutationPriceSerializer(many=True)

    def create(self, validated_data):
        item_prices = validated_data.pop('item_prices')
        item = Item.objects.create(**validated_data)
        for price in item_prices:
            Price.objects.create(item_id=item, **price)

    def update(self, instance, validated_data):
        instance.expirable = validated_data.get('expirable', instance.expirable)
        instance.name = validated_data.get('name', instance.name)
        instance.length = validated_data.get('length', instance.length)
        # todo также нужно дописать изменения permissions
        instance.save()
        return instance

    class Meta:
        model = Item
        fields = ['expirable', 'name', 'length', 'permissions']


class ItemSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all())
    item_prices = MutationPriceSerializer(many=True)

    class Meta:
        model = Item
        fields = '__all__'
