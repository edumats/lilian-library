from django import forms

class isbnForm(forms.Form):
    isbn = forms.CharField(label="ISBN number")
