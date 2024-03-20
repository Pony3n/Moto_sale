from django.db import models

from motorcycles.models import Motorcycle
from moto_user.models import MotoUser


class Cart(models.Model):
    user = models.ForeignKey(MotoUser, on_delete=models.CASCADE)
    motorcycles = models.ManyToManyField(Motorcycle, through='CartItem')
    delivery_address = models.TextField(blank=True, null=True)

    def total_price(self):
        cart_items = self.cartitem_set.all()
        total = sum(item.quantity * item.motorcycle.price for item in cart_items)
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def price(self):
        return self.motorcycle.price * self.quantity

    def __str__(self):
        return f'Лот: {self.motorcycle}'
