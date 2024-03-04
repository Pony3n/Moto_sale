from datetime import date
from PIL import Image
import os

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator, EmailValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class MotoUserManager(BaseUserManager):
    """ Менеджер для моей модели пользователей """

    def create_user(self,
                    email,
                    login,
                    first_name,
                    last_name,
                    date_of_birth,
                    preferences,
                    phone_number,
                    password=None,
                    **extra_fields):
        """
        Метод создания пользователя.
        Включает в себя проверку email и его привидения в нижний регистр.
        Установку пароля и сохранение в БД пользователя.
         """
        if not email:
            raise ValueError('Указание email - обязательно')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          login=login,
                          first_name=first_name,
                          last_name=last_name,
                          date_of_birth=date_of_birth,
                          preferences=preferences,
                          phone_number=phone_number,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, login, password=None, **extra_fields):
        """
        Метод призванный создать супер-пользователя через модель обычного пользователя.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email=email, login=login, password=password, **extra_fields)

    def validate_password_complexity(self, password):
        """ Встроенная валидация Пароля """
        if len(password) < 8:
            raise ValidationError('Пароль должен быть длиннее 8 символов.')
        if not any(char.isdigit() for char in password):
            raise ValidationError('Хотя бы 1 символ должен быть цифрой')
        if not any(char.isalpha() for char in password):
            raise ValidationError('Хотя бы 1 символ должен быть буквой')


class MotoUser(AbstractBaseUser, PermissionsMixin):
    """
    Модель пользователя сайта.
    Включает в себя поля необходимые для создания объекта пользователя
    """
    TYPE_CHOICES = [
        ("КЛАС", "Классика"),
        ("СП", "Спортивный Мотоцикл"),
        ("КР", "Круизер"),
        ("ТМ", "Тяжелый Мотоцикл"),
        ("КРОС", "Кроссовый Мотоцикл"),
        ("ЭН", "Туристический Эндуро"),
        ("ПТ", "Питбайк"),
    ]
    email = models.EmailField(unique=True,
                              validators=[EmailValidator(message='Введите корректный адрес электронной почты.')])
    login = models.CharField(max_length=30, unique=True)
    avatar = models.ImageField(upload_to='moto_user/avatars', blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(
        validators=[
            MinValueValidator(limit_value=date(1900, 1, 1),
                              message='Дата рождения не может быть ранее 1900 года.'),
            MaxValueValidator(limit_value=date.today(),
                              message='Дата рождения не может быть в будущем.'),
        ]
    )
    preferences = models.CharField(max_length=100,
                                   blank=False,
                                   choices=TYPE_CHOICES,
                                   verbose_name='Предпочитаемый вид мотоциклов')
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?7?\d{9,15}$',
                message="Номер телефона должен быть в формате: '+999999999'. Максимум 15 цифр.",
            ),
        ],
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MotoUserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'date_of_birth', 'preferences', 'phone_number']

    password_validator = RegexValidator(
        regex=r'^(?=.*\d)(?=.*[a-zA-Z]).{8,}$',
        message='Пароль должен содержать хотя бы одну цифру и одну букву. Минимум 8 символов.',
        code='invalid_password'
    )

    def save(self, *args, **kwargs):
        """
        Метод который ресайзит полученную картинку, а в случае её отсутствия,
        устанавливает дефолтную
        """
        super().save(*args, **kwargs)
        if self.avatar:
            self.resize_avatar()
        else:
            self.set_default_avatar()

    def resize_avatar(self, *args, **kwargs):
        """
        Метод для ресайзинга аватарки
        """
        image = Image.open(self.avatar.path)
        new_size = (100, 200)
        image.thumbnail(new_size)
        image.save(self.avatar.path)

    def set_default_avatar(self, *args, **kwargs):
        """
        Метод установки дефолтной картинки
        """
        default_avatar_path = os.path.join('/home/druce/IT_stuff/django_moto_seller/moto_seller/'
                                           'moto_user/static/moto_user/images/hz.jpg')
        image = Image.open(default_avatar_path)
        new_size = (100, 200)
        image.thumbnail(new_size)
        default_avatar_path_resized = os.path.join('/home/druce/IT_stuff/django_moto_seller/'
                                                   'moto_seller/media/images/hz_default.jpg')
        image.save(default_avatar_path_resized)
        self.avatar = 'images/hz_default.jpg'
        self.save(update_fields=['avatar'])

    def get_full_name(self):
        """ Метод, который суммирует имя и фамилий и возвращает их вместе """
        return f'{self.first_name} {self.last_name}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('password').validators.append(self.password_validator)

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
