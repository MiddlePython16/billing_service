from payment.api.v1.serializers.item import ItemSerializer
from payment.models import Item, ItemsToUsers, User
from rest_framework import serializers


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

    def create(self, validated_data):
        if self.Meta.model.objects.filter(item_id=validated_data['item_id'],
                                          user_id=validated_data['user_id']).first() is not None:
            raise serializers.ValidationError('User already have this item')

        return super().create(validated_data)

    class Meta:
        model = ItemsToUsers
        exclude = ['id']
        optional_fields = ['user_id']
