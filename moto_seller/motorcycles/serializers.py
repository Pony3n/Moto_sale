from rest_framework import serializers
from .models import Motorcycle


class MotorcycleSerializer(serializers.ModelSerializer):
    """
    Так как корзина написана с использованием DRF, а Motorcycle - модель, которую она использует
    Этот сериализатор, формирует данные мотоциклов для корзины.
    """
    class Meta:
        model = Motorcycle
        fields = ['id',
                  'model_name',
                  'date_of_issue',
                  'moto_type',
                  'engine',
                  'transmission',
                  'status',
                  'seller_comment',
                  'price',
                  'image',
                  ]
