# Generated by Django 5.0.6 on 2024-05-26 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_userregistration_is_active_userregistration_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregistration',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
