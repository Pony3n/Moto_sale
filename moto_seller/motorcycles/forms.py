from django import forms


class MotorcyclesSearchForm(forms.Form):
    search_query = forms.CharField(max_length=90, required=False, label='Найди свою мечту!')