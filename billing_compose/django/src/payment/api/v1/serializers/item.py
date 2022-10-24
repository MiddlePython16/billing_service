from rest_framework import serializers

from payment.models import Item, Permission, Price
from payment.api.v1.serializers.price import PriceSerializer
from payment.api.v1.serializers.permission import PermissionSerializer


class ItemSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, queryset=Permission.objects.all())
    prices = PriceSerializer(many=True, queryset=Price.objects.all())

    class Meta:
        model = Item
        fields = '__all__'
