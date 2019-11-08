import re
import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.utils import timezone

from .models import Account

text ='Must be between 6-8 chars and must contain atleast one uppercase and number'

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

    # def clean_email(self):
    #     # if self.is_valid():
    #         email = self.cleaned_data.get('email')
    #         exp = "^[a-zA-Z][a-zA-Z0-9]+((.|-)[a-zA-Z0-9]+)@[a-zA-Z]*((.|-)[a-z,A-Z]+)[.][a-z]{3}$"
    #         if not re.search(exp,str(email)):
    #             raise forms.ValidationError('Invalid Email..')
    #         try:
    #             Account.objects.exclude(pk=self.instance.pk).get(email=email)
    #         except Account.DoesNotExist:
    #             return email
    #         raise forms.ValidationError('Email is Already in Use')
    #
    # def clean_username(self):
    #     # if self.is_valid():
    #         username = self.cleaned_data.get('username')
    #         try:
    #             Account.objects.exclude(pk=self.instance.pk).get(username=username)
    #         except Account.DoesNotExist:
    #             return username
    #         raise forms.ValidationError('Username is Already in Use')

    def clean_dob(self):
        today = timezone.now().date()
        dob = self.cleaned_data.get('dob')
        date = datetime.datetime.strptime(dob,'%Y-%m-%d')
        age = today.year - date.year -((today.month, today.day) < (date.month, date.day))
        if age < 18:
            forms.ValidationError('Users nust be atleast 18 Years old.')
        return dob

class LoginForm(forms.ModelForm):

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

    class Meta:
        model = Account
        fields = (
            'email',
            'password',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exp = "^[a-zA-Z][a-zA-Z0-9]+((.|-)[a-zA-Z0-9]+)@[a-zA-Z]*((.|-)[a-z,A-Z]+)[.][a-z]{3}$"
        if not re.search(exp,str(email)):
            raise forms.ValidationError('Invalid Email..')
        try:
            Account.objects.get(email=email)
        except Account.DoesNotExist:
            raise forms.ValidationError('No such User..')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        user = False
        try:
            user = Account.objects.get(email=email)
        except:
            pass
        if user:
            if not check_password(password,user.password):
                raise forms.ValidationError('Incorrect Password')
        return password

    def clean(self):
        pass

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

    # def clean_email(self):
    #     # if self.is_valid():
    #         email = self.cleaned_data.get('email')
    #         exp = "^[a-zA-Z][a-zA-Z0-9]+((.|-)[a-zA-Z0-9]+)@[a-zA-Z]*((.|-)[a-z,A-Z]+)[.][a-z]{3}$"
    #         if not re.search(exp,str(email)):
    #             raise forms.ValidationError('Invalid Email..')
    #         try:
    #             Account.objects.exclude(pk=self.instance.pk).get(email=email)
    #         except Account.DoesNotExist:
    #             return email
    #         raise forms.ValidationError('Email is Already in Use')
    #
    # def clean_username(self):
    #     # if self.is_valid():
    #         username = self.cleaned_data.get('username')
    #         try:
    #             Account.objects.exclude(pk=self.instance.pk).get(username=username)
    #         except Account.DoesNotExist:
    #             return username
    #         raise forms.ValidationError('Username is Already in Use')
    #
    # # def clean_age
