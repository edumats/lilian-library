from django import forms
from .models import BookInstance, Tag

class isbnForm(forms.Form):
    isbn = forms.CharField(label="ISBN number")


class bookNoteForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['note']


class tagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
