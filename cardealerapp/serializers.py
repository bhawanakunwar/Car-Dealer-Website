from rest_framework import serializers
#from .models import ContactFormSubmission1
from .models import ContactFormSubmission
from .models import LoanApplication,Car


    
class ContactFormSubmissionSerializer(serializers.ModelSerializer):
     selected_car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
    
     class Meta:
        model = ContactFormSubmission
        fields = ['id', 'name', 'email', 'phone','selected_car', 'message', 'created_at',]
# serializers.py
class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['name', 'model'] 
class LoanApplicationSerializer(serializers.ModelSerializer):
     selected_car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
     
    
     class Meta:
        model = LoanApplication
        fields = ['id', 'name', 'email', 'phone','selected_car', 'message', 'status',]
