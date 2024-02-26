from datetime import date

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator, EmailValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from ..motorcycles.models import Motorcycle


class CustomUserManager(BaseUserManager):

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

    def create_superuser(self,
                         email,
                         login,
                         first_name,
                         last_name,
                         date_of_birth,
                         preferences,
                         phone_number,
                         password=None,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email,
                                login,
                                first_name,
                                last_name,
                                date_of_birth,
                                preferences,
                                phone_number,
                                password,
                                **extra_fields)

    def validate_password_complexity(self, password):
        if len(password) < 8:
            raise ValidationError('Пароль должен быть длиннее 8 символов.')
        if not any(char.isdigit() for char in password):
            raise ValidationError('Хотя бы 1 символ должен быть цифрой')
        if not any(char.isalpha() for char in password):
            raise ValidationError('Хотя бы 1 символ должен быть буквой')


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,
                              validators=[EmailValidator(message='Введите корректный адрес электронной почты.')])
    login = models.CharField(max_length=30, unique=True)
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
                                   choices=Motorcycle.TYPE_CHOICES,
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

    objects = CustomUserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'date_of_birth', 'preferences', 'phone_number']

    password_validator = RegexValidator(
        regex=r'^(?=.*\d)(?=.*[a-zA-Z]).{8,}$',
        message='Пароль должен содержать хотя бы одну цифру и одну букву. Минимум 8 символов.',
        code='invalid_password'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('password').validators.append(self.password_validator)

    def __str__(self):
        return self.login
