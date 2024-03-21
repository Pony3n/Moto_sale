from django import forms


class DeliveryAddressForm(forms.Form):
    """
    Форма позволяющая менять адрес.
    """
    delivery_address = forms.CharField(label='Aдрес доставки',
                                       widget=forms.Textarea,
                                       )
