from payment.models import Permission
from rest_framework import serializers


class MutationPermissionSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Permission.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.json_data = validated_data.get('json_data', instance.json_data)
        instance.save()
        return instance

    class Meta:
        model = Permission
        fields = '__all__'
        exclude = 'id'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
