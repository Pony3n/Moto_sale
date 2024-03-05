from django.contrib.auth import authenticate
from django import forms

from .models import MotoUser


class MotoUserCreationForm(forms.ModelForm):

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
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class MotoUserLoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
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
