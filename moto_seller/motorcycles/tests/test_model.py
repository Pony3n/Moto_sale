import os.path
import re
from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.core.exceptions import ValidationError

from motorcycles.models import Motorcycle, YearField, validate_price
from moto_user.models import MotoUser


class MotorcycleModelTest(TestCase):
    """
    Тесты для модели Мотоциклов
    """

    def setUp(self):
        """
        Метод, в котором создается пользователь для использования в тестах.
        """
        self.user = MotoUser.objects.create(
            email='test@example.com',
            login='Test login',
            avatar='images/hz_default.jpg',
            first_name='Test first name',
            last_name='Test last name',
            date_of_birth=date(2011, 1, 1),
            preferences='ТМ',
            phone_number='+71234567891',
            password='testuser1234'
        )

    def test_base_motorcycle_creation_correct_data(self):
        """
        Проверка создания базового мотоцикла с тестовыми параметрами
        """
        default_image_path = 'motorcycles/static/motorcycles/images/default_moto.jpg'
        moto = Motorcycle.objects.create(
            model_name='Test model name',
            moto_type='СП',
            date_of_issue=1999,
            engine='Test engine',
            transmission=6,
            status=True,
            price=Decimal('10000.0'),
            seller_comment='Test seller comment',
            image=default_image_path,
            creator=self.user
        )
        self.assertEqual(moto.model_name, 'Test model name')
        self.assertEqual(moto.moto_type, 'СП')
        self.assertEqual(moto.date_of_issue, 1999)
        self.assertEqual(moto.engine, 'Test engine')
        self.assertEqual(moto.transmission, 6)
        self.assertTrue(moto.status)
        self.assertEqual(moto.price, Decimal('10000.0'))
        self.assertEqual(moto.seller_comment, 'Test seller comment')
        self.assertEqual(moto.image, default_image_path)
        self.assertEqual(moto.creator, self.user)

    def test_save_method_default_image(self):
        """
        Проверка метода, который устанавливает картинку по умолчанию,
        в случае отсутствия передачи таковой, при создании объекта.
        """
        media_default_image_path = 'media/images/default_moto.jpg'
        moto = Motorcycle.objects.create(
            model_name='Test model name',
            moto_type='СП',
            date_of_issue=1999,
            engine='Test engine',
            transmission=6,
            status=True,
            price=Decimal('10000.0'),
            seller_comment='Test seller comment',
            creator=self.user
        )
        self.assertTrue(moto.image)
        pattern = r'default_moto'
        moto_image_match = re.search(pattern, os.path.basename(moto.image.url))
        media_default_image_match = re.search(pattern, os.path.basename(media_default_image_path))
        self.assertEqual(moto_image_match.group(0), media_default_image_match.group(0))
        image_path = moto.image.path
        moto.delete()
        os.remove(image_path)

    def test_validation_price(self):
        """
        Проверка валидатора цены
        """
        invalid_numbers = ['-1', '-10000', '-0.1', '-0,1', -100, -1, -0.1, 'das']
        for number in invalid_numbers:
            with self.assertRaises(ValidationError):
                validate_price(number)


class YearFieldTest(TestCase):
    """
    Тесты для проверки поля года
    """

    def test_valid_year(self):
        """
        Тесты корректных годов
        """
        field = YearField()
        valid_years = [1900, 1999, 2022, 2024]
        for year in valid_years:
            try:
                field.validate_year(year, None)
            except ValidationError:
                self.fail(f'Год {year} в тесте test_valid_year не прошел проверку')

    def test_invalid_year(self):
        """
        Тест некорректных годов
        """
        field = YearField()
        invalid_years = [1899, 2025, 1700, 2500]
        for year in invalid_years:
            with self.assertRaises(ValidationError):
                field.validate_year(year, None)

