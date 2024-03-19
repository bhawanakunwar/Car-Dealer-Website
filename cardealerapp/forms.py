from django import forms
from .models import TestDrive,ServiceBooking
from .models import Car

class TestDriveForm(forms.ModelForm):
    car = forms.ChoiceField(choices=[], required=True)
    class Meta:
        model = TestDrive
        fields = ['customer_name', 'car', 'date', 'time', 'location', 'address']
    def __init__(self, *args, **kwargs):
        super(TestDriveForm, self).__init__(*args, **kwargs)
        # Populate the car name choices from the database
        car_choices = [(car.car_name, car.car_name) for car in Car.objects.all()]  # Assuming Car model has a 'name' field
        self.fields['car'].choices = car_choices
class ServiceBookingForm(forms.ModelForm):
    car = forms.ChoiceField(choices=[], required=True)
    class Meta:
        model = ServiceBooking
        fields = ['customer_name', 'car', 'service_type', 'date', 'time', 'location','address','comments',]
    def __init__(self, *args, **kwargs):
        super(ServiceBookingForm, self).__init__(*args, **kwargs)
        # Populate the car name choices from the database
        car_choices = [(car.car_name, car.car_name) for car in Car.objects.all()]  # Assuming Car model has a 'name' field
        self.fields['car'].choices = car_choices
# forms.py

from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    message = forms.CharField(widget=forms.Textarea)
