from django import forms


class CartItemQuantityForm(forms.Form):
    cart_item_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1)


class DeliveryAddressForm(forms.Form):
    delivery_address = forms.CharField(label='Aдрес доставки',
                                       widget=forms.Textarea,
                                       )
