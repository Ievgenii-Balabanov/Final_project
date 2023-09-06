from django import forms
from django.contrib.auth.forms import AuthenticationForm

from shop.models import User, Product, Order

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 6)]


class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=40, required=True)


class ParForm(forms.ModelForm):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    class Meta:
        model = Product  # Your Part model
        fields = ["quantity"]


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'delivery_address', 'postal_code', 'city']
