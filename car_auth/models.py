# models.py in your app

from django.contrib.auth.models import AbstractUser
from django.db import models
# models.py or any other file with a reference to the user model

# models.py or any other file with a reference to the user model


class CustomUser(AbstractUser):
   mob_number = models.CharField(max_length=15, blank=True, null=True)
   email = models.EmailField(unique=True)
   is_email_verified=models.BooleanField(default=False)
   def __str__(self):
    return f"{self.email} - {self.mob_number}"
   class Meta:
       db_table="customUser"
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['username']
# models.py in your app (e.g., car_dealer)


