from django import forms

class isbnForm(forms.Form):
    isbn = forms.CharField(label="ISBN number", max_length=13)