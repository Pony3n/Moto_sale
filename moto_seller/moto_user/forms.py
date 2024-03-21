from django.contrib.auth import authenticate
from django import forms

from .models import MotoUser
from motorcycles.models import Motorcycle


class MotoUserCreationForm(forms.ModelForm):
    """
    Форма для создания пользователя.
    Пароль указывается дважды.
    """

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MotoUser
        fields = ['email',
                  'login',
                  'first_name',
                  'last_name',
                  'date_of_birth',
                  'preferences',
                  'phone_number',
                  'avatar',]

    def clean_password2(self):
        """
        Метод отслеживающий совпадения паролей.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class MotoUserLoginForm(forms.Form):
    """
    Форма отвечающая за авторизацию пользователей.
    В случае неверных данных(которых нет в БД) выводит сообщение об ошибке и позволяет попробовать снова.
    """
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = None
        self.request = kwargs.pop('request', None)
        super(MotoUserLoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        login = self.cleaned_data.get('login')
        password = self.cleaned_data.get('password')

        user = authenticate(request=self.request, username=login, password=password)

        if user is None or not user.is_active:
            raise forms.ValidationError("Неверные учетные данные. Пожалуйста, попробуйте снова.")

        self.user = user
        return self.cleaned_data

    def get_user(self):
        return self.user if hasattr(self, 'user') else None


class MotoUserCreateMotorcycleForm(forms.ModelForm):
    """
    Форма для создания мотоцикла пользователем.
    """
    class Meta:
        model = Motorcycle
        fields = ['model_name',
                  'moto_type',
                  'date_of_issue',
                  'engine',
                  'transmission',
                  'status',
                  'price',
                  'seller_comment',
                  'image'
                  ]
        widgets = {
            'moto_type': forms.Select(choices=Motorcycle.TYPE_CHOICES)
        }
