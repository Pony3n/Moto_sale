# Generated by Django 5.0.1 on 2024-02-07 15:28

import motorcycles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Motorcycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=100, verbose_name='Название модели')),
                ('moto_type', models.CharField(choices=[('КЛАС', 'Классика'), ('СП', 'Спортивный Мотоцикл'), ('КР', 'Круизер'), ('ТМ', 'Тяжелый Мотоцикл'), ('КРОС', 'Кроссовый Мотоцикл'), ('ЭН', 'Туристический Эндуро'), ('ПТ', 'Питбайк')], max_length=100, verbose_name='Тип мотоцикла')),
                ('date_of_issue', motorcycles.models.YearField(verbose_name='Дата производства')),
                ('engine', models.CharField(max_length=100, verbose_name='Двигатель')),
                ('transmission', models.IntegerField(verbose_name='Коробка передач')),
                ('status', models.BooleanField(verbose_name='В наличии')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[motorcycles.models.validate_price], verbose_name='Цена в рублях')),
                ('seller_comment', models.TextField(blank=True, verbose_name='Комментарий продавца')),
                ('image', models.ImageField(blank=True, default='motorcycles/images/default_moto.jpg', null=True, upload_to='images/')),
            ],
            options={
                'verbose_name': 'Мотоцикл',
                'verbose_name_plural': 'Мотоциклы',
            },
        ),
    ]
