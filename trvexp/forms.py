from django import forms
from django.core.validators import RegexValidator

class RegistrationForm(forms.Form):
    email = forms.EmailField()
    firstName = forms.CharField(max_length=255, validators=[RegexValidator(r'^[a-zA-Z]+$', 'Only alphabetic characters are allowed.')])
    lastName = forms.CharField(max_length=255, validators=[RegexValidator(r'^[a-zA-Z]+$', 'Only alphabetic characters are allowed.')])
    password = forms.CharField(widget=forms.PasswordInput, min_length=5)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=5)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match")

        # Validate password complexity
        if password:
            if not any(char.isdigit() for char in password):
                raise forms.ValidationError("Password must contain at least one numeral.")
            if not any(char.islower() for char in password):
                raise forms.ValidationError("Password must contain at least one lowercase letter.")
            if not any(char.isupper() for char in password):
                raise forms.ValidationError("Password must contain at least one uppercase letter.")
            if not any(char in '!@#$%^&*()_+' for char in password):
                raise forms.ValidationError("Password must contain at least one symbol: !@#$%^&*()_+")
        return cleaned_data

class LoginForm(forms.Form):
    email_or_userId = forms.CharField(label='Email or UserID')
    password = forms.CharField(widget=forms.PasswordInput)


class SearchForm(forms.Form):
    place_name = forms.CharField(label='Place Name', max_length=100)