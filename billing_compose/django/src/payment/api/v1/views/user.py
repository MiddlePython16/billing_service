from payment.api.v1.serializers.user import UserSerializer
from payment.api.v1.views.__base__ import CustomPaginator
from payment.models import User
from rest_framework import generics


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = CustomPaginator


class UserRetrieveView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
