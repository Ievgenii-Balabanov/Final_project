from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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


class ContactUsForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_from_email(self):
        data = self.cleaned_data["from_email"]

        if data.strip().endswith("mail.ru"):
            raise ValidationError(_("Incorrect! Domain name 'mail.ru' is forbidden"))
        return data

    def clean(self):
        email = self.cleaned_data["from_email"]
        subject = self.cleaned_data["subject"]

        if email.endswith("gmail.com") and "spam" in subject.lower():
            self.add_error(None, "Can't send spam emails")

