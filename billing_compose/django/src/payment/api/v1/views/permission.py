from payment.api.v1.serializers.permission import PermissionSerializer
from payment.api.v1.views.__base__ import CustomPaginator
from payment.models import Permission
from rest_framework import generics


class PermissionCreateView(generics.CreateAPIView):
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()


class PermissionListView(generics.ListAPIView):
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    pagination_class = CustomPaginator


class PermissionRetrieveView(generics.RetrieveAPIView):
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()


class PermissionUpdateView(generics.UpdateAPIView):
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()


class PermissionDestroyView(generics.DestroyAPIView):
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
