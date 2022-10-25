from rest_framework import serializers

from payment.api.v1.serializers.item import ItemSerializer
from payment.models import User, Item, ItemsToUsers


class MutationUserSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, queryset=Item.objects.all())

    class Meta:
        model = User
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'


class MutationItemsToUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemsToUsers
        exclude = ['id']
        optional_fields = ['user_id']
