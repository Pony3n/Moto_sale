from django.db import models

from motorcycles.models import Motorcycle
from moto_user.models import MotoUser


class Cart(models.Model):
    """
    Модель корзины, включает в себя поля: пользователя, мотоциклов и адрес доставки.
    Так же добавлен метод подсчета цены всех мотоциклов в корзине.
    """
    user = models.ForeignKey(MotoUser, on_delete=models.CASCADE)
    motorcycles = models.ManyToManyField(Motorcycle, through='CartItem')
    delivery_address = models.TextField(blank=True, null=True)

    def total_price(self):
        cart_items = self.cartitem_set.all()
        total = sum(item.quantity * item.motorcycle.price for item in cart_items)
        return total


class CartItem(models.Model):
    """
    Класс отвечающий за объекты в корзине.
    Помимо полей корзины(к которой относится объект), мотоцикла и количества,
    Так же имеет метода подсчета общей стоимости мотоцикла в указанном количестве.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def price(self):
        return self.motorcycle.price * self.quantity

    def __str__(self):
        return f'Лот: {self.motorcycle}'

    def get_model_name(self):
        return self.motorcycle.model_name