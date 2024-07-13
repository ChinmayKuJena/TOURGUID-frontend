from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.core.validators import RegexValidator



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
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, first_name,last_name, password, **extra_fields)
    

# userobject 
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
    token_expiration = models.DateTimeField(null=True, blank=True)  # New field for token expiration
    last_logout = models.DateTimeField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    
    # def __str__(self):
    #     return self.username

# for image and blog obj
class ImageBlogModel(models.Model):
    
    state_name = models.CharField(max_length=255)
    state_id = models.CharField(max_length=10)
    place_name = models.CharField(max_length=255)
    place_id = models.CharField(max_length=10)
    username = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    blog = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.place_name} - {self.username}"    
    



# class Place1(models.Model):
#     placeid = models.AutoField(primary_key=True)
#     stateid = models.CharField(max_length=2, blank=True, null=True)
#     placename = models.CharField(max_length=255)
#     placedetails = models.CharField(max_length=255)

#     class Meta:
#         db_table = 'place'


# class States(models.Model):
#     id = models.CharField(primary_key=True, max_length=20)
#     state = models.CharField(max_length=50)
#     famousfor = models.CharField(max_length=100)
#     class Meta:
#         db_table = 'india'
#     # def __str__(self):
#     #     return self.state

# class Place2(models.Model):
#     placeid = models.AutoField(primary_key=True)
#     stateid = models.ForeignKey(States, on_delete=models.CASCADE)
#     placename = models.CharField(max_length=255)
#     placedetails = models.CharField(max_length=255)

#     def __str__(self):
#         return self.placename

