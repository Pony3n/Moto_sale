import datetime

from django.core.exceptions import ValidationError
from django.db import models


def validate_price(value):
    if value is not None:
        value = str(value).replace(' ', '')  # удаляем пробелы
        if not value.replace('.', '', 1).isdigit():  # проверяем, что значение состоит только из цифр и может содержать только одну точку
            raise ValidationError('Цена должна содержать только цифры и может содержать только одну точку')


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
    model_name = models.CharField(max_length=100, blank=False, verbose_name='Название модели')
    moto_type = models.CharField(max_length=100, blank=False, verbose_name='Тип мотоцикла')
    date_of_issue = YearField(blank=False, verbose_name='Дата производства')
    engine = models.CharField(max_length=100, blank=False, verbose_name='Двигатель')
    transmission = models.IntegerField(blank=False, verbose_name='Коробка передач')
    status = models.BooleanField(verbose_name='В наличии')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        verbose_name="Цена в рублях",
        validators=[validate_price])
    seller_comment = models.TextField(blank=True, verbose_name='Комментарий продавца')
    image = models.ImageField(blank=False, default='default_moto.jpg', upload_to='images/')

    def __str__(self):
        return self.model_name

    class Meta:
        verbose_name = 'Мотоцикл'
        verbose_name_plural = 'Мотоциклы'

#TODO Написать так поле price, чтобы оно принимало значения с пробелами между цифр

