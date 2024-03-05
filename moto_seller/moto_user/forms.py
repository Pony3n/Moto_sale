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