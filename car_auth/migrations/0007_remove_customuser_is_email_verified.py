# Generated by Django 4.2.3 on 2024-03-22 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car_auth', '0006_customuser_is_email_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_email_verified',
        ),
    ]
