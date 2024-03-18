from rest_framework import serializers

from motorcycles.serializers import MotorcycleSerializer
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    motorcycle = MotorcycleSerializer()
    user_login = serializers.ReadOnlyField(source='cart.user.login')

    class Meta:
        model = CartItem
        fields = ['id', 'user_login', 'motorcycle', 'quantity', 'price']


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    motorcycles = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_motorcycles(self, obj):
        return [motorcycle.model_name for motorcycle in obj.motorcycles.all()]

    def get_user(self, obj):
        return obj.user.login if obj.user else None

    class Meta:
        model = Cart
        fields = ['id', 'user', 'motorcycles', 'delivery_address', 'cart_items']

