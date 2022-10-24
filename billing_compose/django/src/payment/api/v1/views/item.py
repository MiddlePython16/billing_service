from payment.api.v1.serializers.item import ItemSerializer, MutationItemSerializer
from payment.api.v1.views.__base__ import CustomPaginator
from payment.models import Item
from rest_framework import generics


class ItemCreateView(generics.CreateAPIView):
    serializer_class = MutationItemSerializer
    queryset = Item.objects.all()


class ItemListView(generics.ListAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    pagination_class = CustomPaginator


class ItemRetrieveView(generics.RetrieveAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


class ItemUpdateView(generics.UpdateAPIView):
    serializer_class = MutationItemSerializer
    queryset = Item.objects.all()


class ItemDestroyView(generics.DestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
