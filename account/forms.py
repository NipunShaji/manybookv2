import re
import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.utils import timezone

from .models import Account

class RegistrationForm(UserCreationForm):

    class Meta:
        model = Account
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'dob',
            'userpic',
        )

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
        }
    ))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
        }
    ))

    email = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            "placeholder":'someone@mail.com',
        }
    ))

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            "placeholder":'walter',
        }
    ))

    dob = forms.CharField(widget=forms.DateInput(
        attrs={
            'class':'form-control',
            "placeholder":'YYYY-MM-DD',
            'type':'date',
        }
    ))

    def clean_dob(self):
        today = timezone.now().date()
        dob = self.cleaned_data.get('dob')
        date = datetime.datetime.strptime(dob,'%Y-%m-%d')
        age = today.year - date.year -((today.month, today.day) < (date.month, date.day))
        if age < 18:
            forms.ValidationError('Users nust be atleast 18 Years old.')
        return dob

class LoginForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = (
            'email',
            'password',
        )

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            "placeholder":'Password',
        }
    ))

    email = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            "placeholder":'Email: someone@mail.com',
        }
    ))

class UpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = (
            'email',
            'username',
            'dob',
            'userpic',
        )

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            "placeholder":'username',
        }
    ))

    email = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            "placeholder":'Email: someone@mail.com',
        }
    ))

    dob = forms.CharField(widget=forms.DateInput(
        attrs={
            'class':'form-control',
            "placeholder":'YYYY-MM-DD',
            'type':'date',
        }
    ))
