from django.utils import timezone
from django.db import models
from django.core.validators import RegexValidator
import random

class UserTable(models.Model):
    only_alphabets_validator = RegexValidator(
        regex=r'^[a-zA-Z]+$',
        message='Only alphabetic characters are allowed.',
        code='invalid_alphabets'
    )

    userId = models.CharField(primary_key=True, max_length=255, unique=True, editable=False)
    email = models.EmailField(unique=True, null=False)
    firstName = models.CharField(max_length=255, null=True, blank=True, validators=[only_alphabets_validator])
    lastName = models.CharField(max_length=255, null=True, blank=True, validators=[only_alphabets_validator])
    userName = models.CharField(max_length=255, null=False, blank=False)
    password = models.CharField(max_length=255, null=False)
    joinDate = models.DateTimeField(default=timezone.now, null=False)
    lastloginDate = models.DateTimeField(null=True, blank=True)
    lastlogoutDate = models.DateTimeField(null=True, blank=True)
    jwtToken = models.TextField(null=True, blank=True)
    jwtExpTime = models.DateTimeField(null=True, blank=True)
    new = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Generate userId
        random_id = ''.join([str(random.randint(0, 9)) for _ in range(5)])
        if not self.userId:
            self.userId = f"TRV_EXP{random_id}"

        # Set userName as firstName + lastName
        if not self.userName:
            self.userName = f"{self.firstName} {self.lastName} {random_id}"

        super(UserTable, self).save(*args, **kwargs)

    def __str__(self):
        return self.userName or self.email
