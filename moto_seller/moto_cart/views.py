from rest_framework import viewsets
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .forms import DeliveryAddressForm
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from motorcycles.models import Motorcycle


class CartViewSet(viewsets.ModelViewSet):
    """
    Представление отвечающее за отображение данных о корзине в формате JSON.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class CartItemViewSet(viewsets.ModelViewSet):
    """
    Представление отвечающее за отображение данных об объектах в корзине в формате JSON.
    """
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


class MotoUserCartView(LoginRequiredMixin, View):
    """
    Представление отвечающее за отображение корзины пользователю.
    Так же позволяет пользователю на этой странице добавить адрес доставки.
    """
    template_name = 'moto_cart/moto_user_cart.html'

    def get(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(cart__user=request.user)
        cart = Cart.objects.get_or_create(user=request.user)[0]
        form = DeliveryAddressForm(initial={'delivery_address': cart.delivery_address})
        context = {
            'cart_items': cart_items,
            'form': form,
            'delivery_address': cart.delivery_address,
            'cart': cart
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        """
        Метод, позволяющий пользователю обновить адрес доставки, затем
        обновляет страницу с актуальными данными.
        """
        form = DeliveryAddressForm(request.POST)
        if form.is_valid():
            cart = Cart.objects.get_or_create(user=request.user)[0]
            cart.delivery_address = form.cleaned_data['delivery_address']
            cart.save()
            return redirect('moto_user_cart')

