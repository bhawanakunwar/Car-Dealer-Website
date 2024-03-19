from django.db import models
from django.conf import settings
from car_auth.models import CustomUser


from django.db import models

from django.db import models

class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
    ]
    #id = models.AutoField(primary_key=True,default="0")
    car_name = models.CharField(max_length=50, default="")
    category = models.CharField(max_length=100, default="")
    price = models.IntegerField(default=0)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    transmission_type = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES,default="automatic")
    image = models.ImageField(upload_to='images/', default="")
    description = models.TextField()

    def __str__(self):
        return f"{self.car_name} {self.price} {self.year} {self.transmission_type}"

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
    customer_name = models.CharField(max_length=100)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES)
    date = models.DateField()
    time = models.CharField(max_length=100) 
    location = models.CharField(max_length=10, choices=LOCATION_CHOICES, default='carzone')
    address = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
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
    customer_name = models.CharField(max_length=100)  
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=100) 
    location = models.CharField(max_length=10, choices=LOCATION_CHOICES, default='carzone')
    address = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    
    def __str__(self):
        return f"Test Drive of {self.car} at {self.location} on {self.date} from {self.time}"

class Financier(models.Model):
    name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    email = models.EmailField()
    contact_number = models.CharField(max_length=20)
    website = models.URLField()
    logo = models.ImageField(upload_to='financier_logos/')
    description = models.TextField()
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

class Order(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,default="")
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    delivery_location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20)
    order_status = models.CharField(max_length=20)
    additional_information = models.TextField(blank=True)

    def __str__(self):
        return self.order_id
