from django import forms
from .models import MotoUser


class MotoUserCreationForm(forms.ModelForm):
    class Meta:
        model = MotoUser
        fields = ['email',
                  'login',
                  'first_name',
                  'last_name',
                  'date_of_birth',
                  'preferences',
                  'phone_number',
                  'avatar']
