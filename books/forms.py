from django import forms

from .models import Book
from account.models import Account


class AddBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            'title',
            'author',
            'series',
            'language',
            'isbn',
            'file',
            'genre',
            'cover',
            'description',
            'user'
        )

    title  = forms.CharField(widget=forms.TextInput(
            attrs={
                'class':'formcontrol itemToBeFocused',
                'required':'false',
            }
        ))

    author  = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'formcontrol itemToBeFocused',
        }
    ))

    series  = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'formcontrol itemToBeFocused',
        }
    ))

    isbn  = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'formcontrol itemToBeFocused',
        }
    ))

    description = forms.CharField(widget=forms.Textarea())

    def save(self):
        instance  = super(AddBook, self).save()
        instance.genre.clear()
        instance.genre.add(*self.cleaned_data['genre'])
        return instance
