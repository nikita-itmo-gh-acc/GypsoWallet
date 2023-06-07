from django import forms
from exchange.models import *
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Введите пароль"}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Повторите пароль"}))

    class Meta:
        model = User
        fields = ("username", "email")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Логин"}),
            "email": forms.TextInput(attrs={"placeholder": "Почта"})
        }

    def clean_password_repeat(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_repeat']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password_repeat']


class LoginForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Логин"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Введите пароль"}))


class ProfileForm(forms.ModelForm):
    # avatar = forms.ImageField()
    # description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "О себе"}))

    class Meta:
        model = Profile
        fields = ("photo", "description")
        widgets = {
            "description": forms.Textarea(attrs={"placeholder": "О себе", "form": "profile_form"})
        }


