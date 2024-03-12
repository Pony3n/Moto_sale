from django import forms
from django.core import validators

from moto_cart.models import CartItem
from .models import Motorcycle


class MotorcyclesSearchForm(forms.Form):
    TYPE_CHOICES = Motorcycle.TYPE_CHOICES
    search_query = forms.CharField(max_length=90, required=False, label='Найди свою мечту!')
    min_date_of_issue = forms.IntegerField(
        label='Мин. дата производства',
        required=False,
        widget=forms.Select(choices=[(year, year) for year in range(1950, 2025)]),
    )
    max_date_of_issue = forms.IntegerField(
        label='Макс. дата производства',
        required=False,
        widget=forms.Select(choices=[(year, year) for year in range(2024, 1949, -1)]),
    )

    moto_type = forms.ChoiceField(label='Тип мотоцикла',
                                  required=False,
                                  choices=[('', '---')] + TYPE_CHOICES)
    min_price = forms.DecimalField(label='Мин. цена', required=False)
    max_price = forms.DecimalField(label='Макс. цена', required=False)


class MotoAddToCartForm(forms.ModelForm):
    motorcycle = forms.ModelChoiceField(queryset=Motorcycle.objects.all(), widget=forms.HiddenInput(), required=False)
    quantity = forms.IntegerField(label='Количество',
                                  required=True,
                                  validators=[
                                      validators.MinValueValidator(1, 'Количество должно быть больше 1')
                                  ])

    class Meta:
        model = CartItem
        fields = ['motorcycle', 'quantity']
