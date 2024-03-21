from rest_framework import serializers

from motorcycles.serializers import MotorcycleSerializer
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объектов корзины пользователя.
    """
    motorcycle = MotorcycleSerializer()
    user_login = serializers.ReadOnlyField(source='cart.user.login')

    class Meta:
        model = CartItem
        fields = ['id', 'user_login', 'motorcycle', 'quantity', 'price']


class CartSerializer(serializers.ModelSerializer):
    """
    Сериализатор корзин на сайте.
    """
    cart_items = CartItemSerializer(many=True, read_only=True)
    motorcycles = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_motorcycles(self, obj):
        """
        Метод выводящий название модели мотоцикла, в списке ключа motorcycles.
        Упрощает чтение.
        """
        return [motorcycle.model_name for motorcycle in obj.motorcycles.all()]

    def get_user(self, obj):
        """
        Метод выводящий логин пользователя, как значение для ключа user.
        Упрощает чтение.
        """
        return obj.user.login if obj.user else None

    class Meta:
        model = Cart
        fields = ['id', 'user', 'motorcycles', 'delivery_address', 'cart_items']

