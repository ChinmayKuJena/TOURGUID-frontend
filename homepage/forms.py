from django import forms
from django.core.exceptions import ValidationError

from .models import  UserRegistration,ImageBlogModel

# image and blog form
class ImageBlogForm(forms.ModelForm):
    class Meta:
        model = ImageBlogModel
        fields = ['image', 'blog']

class UserRegistrationForm(forms.ModelForm):
# class UserRegistrationForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserRegistration
        fields = ('email', 'first_name', 'last_name')
    # validate password
    def validate_password(self, password):
        # Custom password validation
        if len(password) < 5:
            raise ValidationError("Password must be at least 5 characters long.")
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one digit.")
        if not any(char in "!@#$%^&*()_+=-{}[]:;\"'<>,.?/\\" for char in password):
            raise ValidationError("Password must contain at least one symbol.")

    def clean_password(self):
        password = self.cleaned_data.get('password')
        self.validate_password(password)
        return password
    # check password and confirm_password same or not 
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # hash password
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = "Password must be at least 5 characters long and contain at least one uppercase letter, one digit, and one symbol."


# login form
class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)  


class SearchForm(forms.Form):
    place_name = forms.CharField(label='Place Name', max_length=100)

