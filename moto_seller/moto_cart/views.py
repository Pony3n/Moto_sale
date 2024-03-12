from rest_framework import generics, viewsets, status
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from motorcycles.models import Motorcycle


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        cart_id = self.kwargs['cart_pk']
        motorcycle_id = self.request.data.get('motorcycle')
        quantity = self.request.data.get('quantity', 1)

        motorcycle = Motorcycle.objects.get(pk=motorcycle_id)
        cart = Cart.objects.get(pk=cart_id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, motorcycle=motorcycle)

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

    def perform_destroy(self, instance):
        instance.delete()

