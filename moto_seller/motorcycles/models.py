import datetime
import os
from decimal import Decimal, DecimalException

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.core.files import File

from moto_user.models import MotoUser


def validate_price(value):          #TODO Неработает валидация
    if isinstance(value, str):
        value = value.replace(',', '').replace(' ', '')
    if value < Decimal('0'):
        raise ValidationError('Цена не может быть отрицательной')
    try:
        value = Decimal(value)
    except (TypeError, ValueError):
        raise ValidationError("Введите корректное значение")


class YearField(models.IntegerField):
    def validate_year(self, value, models_instance):
        super().validate(value, models_instance)
        if value < 1900 or value > datetime.datetime.now().year:
            raise ValidationError('Некорректный год')

    def formfield(self, **kwargs):
        defaults = {"min_value": 1900, "max_value": datetime.datetime.now().year}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class Motorcycle(models.Model):
    TYPE_CHOICES = [
        ("КЛАС", "Классика"),
        ("СП", "Спортивный Мотоцикл"),
        ("КР", "Круизер"),
        ("ТМ", "Тяжелый Мотоцикл"),
        ("КРОС", "Кроссовый Мотоцикл"),
        ("ЭН", "Туристический Эндуро"),
        ("ПТ", "Питбайк"),
    ]
    model_name = models.CharField(max_length=100, blank=False, verbose_name='Название модели')
    moto_type = models.CharField(max_length=100, blank=False, choices=TYPE_CHOICES, verbose_name='Тип мотоцикла')
    date_of_issue = YearField(blank=False, verbose_name='Дата производства')
    engine = models.CharField(max_length=100, blank=False, verbose_name='Двигатель')
    transmission = models.IntegerField(blank=False, verbose_name='Коробка передач')
    status = models.BooleanField(verbose_name='В наличии')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        default=0,
        verbose_name="Цена в рублях",
        validators=[validate_price])
    seller_comment = models.TextField(blank=True, verbose_name='Комментарий продавца')
    image = models.ImageField(blank=True,
                              null=True,
                              upload_to='images/')   #TODO Сделать картинки так, чтобы их можно было отдавать галлереей
    creator = models.ForeignKey(MotoUser, on_delete=models.CASCADE, default=1)

    def save(self, *args, **kwargs):
        if not self.image:
            default_image_path = os.path.join(settings.BASE_DIR, 'motorcycles',
                                              'static',
                                              'motorcycles',
                                              "images",
                                              "default_moto.jpg")
            with open(default_image_path, 'rb') as f:
                self.image.save('default_moto.jpg', File(f), save=False)
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.price:
            cleaned_price = str(self.price).replace(',', '').replace(' ', '')
            try:
                self.price = Decimal(cleaned_price)
            except DecimalException:
                raise ValidationError({'price': "Неверный формат цены"})

    def __str__(self):
        return self.model_name

    class Meta:
        verbose_name = 'Мотоцикл'
        verbose_name_plural = 'Мотоциклы'


#TODO Написать так поле price, чтобы оно принимало значения с пробелами между цифр



