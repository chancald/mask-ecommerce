from django import forms

STATE_CHOICES = (
    ('SA', 'Santo Domingo'),
    ('ST', 'Santiago'),
)
PAYMENT_CHOICES = (
    ('EF', 'Efectivo'),
)

class AddressForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    phone = forms.CharField()
    street_address = forms.CharField(required=False)   
    street_address_2 = forms.CharField(required=False)
    state_option = forms.CharField(required=False, widget=forms.Select(choices=STATE_CHOICES))
    payment_option = forms.ChoiceField(required=False, widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)
    promo_code = forms.CharField(required=False)


class PromoForm(forms.Form):
    promo_code = forms.CharField(required=False)
