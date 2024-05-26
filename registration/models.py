from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from pydantic_core import ValidationError
# for superusers this class
class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name,last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,last_name=last_name, **extra_fields)
        if password:
            # try:
            #     # self.validate_password(password)  # Validate the password
            # except ValidationError as e:
            #     raise ValueError(str(e))  # Raise ValueError with validation error message
            user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name,last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, first_name,last_name, password, **extra_fields)
    


class UserRegistration(AbstractBaseUser):
    only_alphabets_validator = RegexValidator(
        regex=r'^[a-zA-Z]+$',
        message='Only alphabetic characters are allowed.',
        code='invalid_alphabets'
    )

    email = models.EmailField(unique=True)
    # username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=False, validators=[only_alphabets_validator])
    last_name = models.CharField(max_length=30, null=True, blank=False, validators=[only_alphabets_validator])    
    created_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    token = models.CharField(max_length=255, null=True, blank=True)  # Field for token (nullable)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    # def validate_password(self, password):
    #     min_length_validator = RegexValidator(
    #         regex=r'^.{5,}$',
    #         message='Password must be at least 5 characters long.',
    #         code='password_too_short'
    #     )

    #     uppercase_validator = RegexValidator(
    #         regex=r'[A-Z]',
    #         message='Password must contain at least one uppercase letter.',
    #         code='password_no_uppercase'
    #     )

    #     digit_validator = RegexValidator(
    #         regex=r'\d',
    #         message='Password must contain at least one digit.',
    #         code='password_no_digit'
    #     )

    #     symbol_validator = RegexValidator(
    #         regex=r'[!@#$%^&*()_+=\-{}\[\]:;\"\'<>,.?/\\]',
    #         message='Password must contain at least one symbol.',
    #         code='password_no_symbol'
    #     )

    #     min_length_validator(password)
    #     uppercase_validator(password)
    #     digit_validator(password)
    #     symbol_validator(password)
    def __str__(self):
        return self.username
