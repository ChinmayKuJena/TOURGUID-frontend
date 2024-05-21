from django import forms

class SearchForm(forms.Form):
    place_name = forms.CharField(label='Place Name', max_length=100)
