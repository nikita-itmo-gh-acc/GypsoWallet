from django import forms
from exchange.models import *


class RegisterForm(forms.Form):
    # class Meta:
    #     model = User
    #     fields = "__all__"
    login = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Логин"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Почта"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Введите пароль"}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Повторите пароль"}))


class LoginForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Логин"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Введите пароль"}))



