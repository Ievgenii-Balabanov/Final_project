from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from shop.models import User


class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]


# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=50, required=True)
#     password = forms.CharField(max_length=40, required=True)
#     # email = forms.EmailField(required=True)

class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=40, required=True)

