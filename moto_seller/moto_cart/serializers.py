from rest_framework import serializers

from motorcycles.serializers import MotorcycleSerializer
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    motorcycle = MotorcycleSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'motorcycle', 'quantity', 'price']


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'motorcycles', 'delivery_address', 'cart_items']
