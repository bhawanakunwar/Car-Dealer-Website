from django.db import models
from django.conf import settings
from car_auth.models import CustomUser
from django.utils.safestring import mark_safe

from django.db import models

from django.db import models
from datetime import datetime

class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
    ]
    CATEGORY_CHOICES = [
        ('sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('hatchback', 'Hatchback'),
    ]
    MAKE_CHOICES =  [
        ('hyundai', 'Hyundai'),
        ('honda', 'Honda'),
        ('mahindra', 'Mahindra'),
        ('ford', 'Ford'),
        ('kia', 'Kia'),
    ]
    current_year = datetime.now().year
    YEAR_CHOICES = [(year, str(year)) for year in range(current_year - 10, current_year + 1)]

    #id = models.AutoField(primary_key=True,default="0")
    car_name = models.CharField(max_length=50, default="")
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default="")  # Category field with specific choices
    price = models.CharField(max_length=100)
    make = models.CharField(max_length=100, choices=MAKE_CHOICES, default="") 
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField(choices=YEAR_CHOICES)
    transmission_type = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES,default="automatic")
    image = models.ImageField(upload_to='images/', default="")
    description = models.TextField()

    def __str__(self):
        return f"{self.car_name} {self.price} {self.year} {self.transmission_type}"
    def display_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="100" height="auto" />') if self.image else ''
    display_image.short_description = 'Image'
# models.py
from django.utils import timezone
class ServiceBooking(models.Model):
    LOCATION_CHOICES = [
        ('center', 'Center'),
        ('home', 'Home'),
    ]
    SERVICE_TYPE_CHOICES = [
        ('maintenance', 'Maintenance'),
        ('repair', 'Repair'),
        ('inspection', 'Inspection'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('In Progress', 'In Progress'),
    ]
    customer_name = models.CharField(max_length=100)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES)
    date = models.DateField()
    time = models. TimeField()
    location = models.CharField(max_length=10, choices=LOCATION_CHOICES, default='carzone')
    address = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    comments = models.TextField(blank=True, null=True)

    
   

    def __str__(self):
        return f"Service Booking for {self.car} at {self.location} on {self.date} from {self.time}"
# cardealerapp/models.py
from django.utils import timezone


class TestDrive(models.Model):
    LOCATION_CHOICES = [
        ('carzone', 'Carzone Center'),
        ('home', 'Home'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled','Cancelled'),
    ]
    customer_name = models.CharField(max_length=100)  
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(max_length=20)
    location = models.CharField(max_length=10, choices=LOCATION_CHOICES, default='carzone')
    address = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    

def __str__(self):
 return f"Test Drive of {self.car} at {self.location} on {self.date} from {self.time}"

class Financier(models.Model):
    name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    email = models.EmailField()
    contact_number = models.CharField(max_length=20)
    website = models.URLField()
    logo = models.ImageField(upload_to='financier_logos/')
  
# models.py

from django.db import models
from django.contrib.auth.models import User

class Wishlist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    cars = models.ManyToManyField(Car, through='Wishlist_Car')

    def __str__(self):
        return f"Wishlist for {self.user.username}"
    
class Wishlist_Car(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    class Meta:
       
        unique_together = (('wishlist', 'car'),)
from django.db import models

class ContactFormSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    selected_car = models.ForeignKey('Car', on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
from django.db import models

class LoanApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]


    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    selected_car = models.ForeignKey('Car', on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20,  choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('Expired', 'Expired'),
        ('Valid', 'Valid'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateTimeField()
    token_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    order_id = models.CharField(max_length=100,default='')  # Add order_id field
    payment_id = models.CharField(max_length=100,default='')  # Add payment_id field
    token_id = models.CharField(max_length=100,default='')  # Add token_id field
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Valid')
    
    def save(self, *args, **kwargs):
        current_datetime = timezone.now()
        if self.expiration_date < current_datetime:
            self.status = "Expired"
        else:
            self.status = "Valid"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Reservation #{self.id} for {self.user.username}"

import random
import string
class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        
    ]
    ORDER_STATUS_CHOICES = [
        ('Processing', 'Processing'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    order_id = models.CharField(max_length=100,  blank=True,unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default="")
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    delivery_location = models.CharField(max_length=255)
    price = models.CharField(max_length=100, default="")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Processing')
    additional_information = models.TextField(blank=True)
    reservation = models.OneToOneField(Reservation, on_delete=models.SET_NULL, null=True, blank=True)

    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only generate a new order ID if it's a new order
            # Generate order ID
            random_id = ''.join(random.choices(string.digits, k=6))  # Generate a random 6-digit ID
            self.order_id = f"#{random_id}"

        # Set delivery_date to 7 days after order_date if not set
        if not self.delivery_date:
            self.delivery_date = self.order_date + timezone.timedelta(days=7)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id