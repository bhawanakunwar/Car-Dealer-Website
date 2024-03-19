from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import TestDrive, ServiceBooking, Car, Wishlist, ContactFormSubmission, Financier
from math import ceil
from rest_framework import status as rest_framework_status
from .models import LoanApplication
from .models import ContactFormSubmission
from .forms import ServiceBookingForm,TestDriveForm
from datetime import datetime
from django.db.models import Count
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


def index(request):
  featured_cars = Car.objects.all()[:6]  # Adjust the limit as needed
  return render(request, 'index.html', {'featured_cars': featured_cars})


from django.shortcuts import render
from .models import Car

def search(request):
    query = request.GET.get('q')
    results = Car.objects.filter(car_name__icontains=query) if query else []
    return render(request, 'search.html', {'results': results, 'query': query})

razorpay_client = razorpay.Client(auth=("rzp_test_EnQJ2nNXIuo5cM", "Ex59lRId5ZgCAxWWFiqcwiN3"))
@login_required(login_url="/auth/login/")
@csrf_exempt

def book_test_drive(request,car_id=None):
    if request.method == 'POST':
        # Assuming you have a TestDrive model to save the form data
        car_id = request.POST.get('car')
        
        customer_name = request.POST.get('customer_name')
        location = request.POST.get('location')
        address = request.POST.get('address', '') # Address might not be present if location is 'center'
        date = request.POST.get('date')
        time = request.POST.get('time')

        # Save the form data to the database
        test_drive = TestDrive(
            car_id=car_id,
            customer_name=customer_name,
            location=location,
            address=address,
            date=date,
            time=time
        )
        test_drive.save()

        # Return a JSON response indicating success
        return JsonResponse({'success': True})
    else:
        # Handle GET requests for the form here if needed
        available_cars = Car.objects.all()  # Fetch available cars from the database
        return render(request, 'book_test_drive.html', {'available_cars': available_cars})



  

@login_required(login_url="/auth/login")    
def create_razorpay_order(request):
    amount = 999 
    order_data = {
        'amount': amount * 100,  # Razorpay requires amount in paise
        'currency': 'INR',
        'receipt': 'receipt_order_74394',  # You can generate a dynamic receipt ID
    }
    order = razorpay_client.order.create(data=order_data)
    return JsonResponse(order)
def razorpay_callback(request):
    if request.method == 'POST':
        payload = request.body.decode('utf-8')
        return JsonResponse({'status': 'success'}) 





def book_test_drive_from_car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    
    if request.method == 'POST':
    
        customer_name = request.POST.get('customer_name')
        location = request.POST.get('location')
        address = request.POST.get('address', '') # Address might not be present if location is 'center'
        date = request.POST.get('date')
        time = request.POST.get('time')

        # Save the form data to the database
        test_drive = TestDrive(
            car=car,
            customer_name=customer_name,
            location=location,
            address=address,
            date=date,
            time=time
        )
        test_drive.save()

        # Return a JSON response indicating success
        return JsonResponse({'success': True})
    else:
        
        available_cars = Car.objects.all()  # Fetch available cars from the database
     
        
        return render(request, 'book_test_drive.html', {'car':car,'available_cars': available_cars})





@login_required(login_url="/auth/login")     
def test_drive_success(request):
    return render(request, 'test_drive_success.html')
@login_required(login_url="/auth/login") 
def book_service(request,car_id=None):
    if request.method == 'POST':
        # Retrieve form data
        car_id = request.POST.get('car')
        car = get_object_or_404(Car, pk=car_id)
        customer_name = request.POST.get('customer_name')
        location = request.POST.get('location')
        address = request.POST.get('address', '')  # Address might not be present if location is 'center'
        service_type = request.POST.get('service_type')
        date = request.POST.get('date')
        time = request.POST.get('time')
        comments = request.POST.get('comments')

        # Save the form data to the database
        service_booking = ServiceBooking(
            car=car,
            customer_name=customer_name,
            location=location,
            address=address,
            service_type=service_type,
            date=date,
            time=time,
            comments=comments
        )
        service_booking.save()

        # Return a JSON response indicating success
        return JsonResponse({'success': True})
    else:
        # Handle GET requests for the form here if needed
        available_cars = Car.objects.all()  # Fetch available cars from the database
        return render(request, 'book_service.html', {'available_cars': available_cars})


def car_list(request):
    allCars=[]
    catCars=Car.objects.values('category','id')
    cats={item['category']for item in catCars}
    for cat in cats:
        car=Car.objects.filter(category=cat)
        n=len(car)
        nSlides=n // + ceil((n+4)-(n // 4))
        allCars.append([car,range(1,nSlides),(nSlides)])
    params={'allCars':allCars}
    return render(request, 'car_list.html',params)

from .models import Car, Financier
import razorpay
from django.conf import settings
client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))
@login_required(login_url="/auth/login") 
def checkout(request, car_id):
    selected_car = None
    if car_id:
         selected_car = Car.objects.get( pk=car_id)
    financiers = Financier.objects.all()[:3]
    available_cars = Car.objects.all()  
    return render(request, 'checkout.html', {'selected_car': selected_car, 'financiers': financiers,'available_cars': available_cars})

def initiate_payment(amount, currency='INR'):
   data = {
       'amount': amount * 100,  # Razorpay expects amount in paise (e.g., 100 INR = 10000 paise)
       'currency': currency,
       'payment_capture': '1'  # Auto capture the payment after successful authorization
   }
   response = client.order.create(data=data)
   return response['id']


def payment_view(request):
   amount = 100  # Set the amount dynamically or based on your requirements
   order_id = initiate_payment(amount)
   context = {
       'order_id': order_id,
       'amount': amount
   }
   return render(request, 'payment.html', context)

def payment_success_view(request):
   order_id = request.POST.get('order_id')
   payment_id = request.POST.get('razorpay_payment_id')
   signature = request.POST.get('razorpay_signature')
   params_dict = {
       'razorpay_order_id': order_id,
       'razorpay_payment_id': payment_id,
       'razorpay_signature': signature
   }
   try:
       client.utility.verify_payment_signature(params_dict)
       # Payment signature verification successful
       # Perform any required actions (e.g., update the order status)
       return render(request, 'payment_success.html')
   except razorpay.errors.SignatureVerificationError as e:
       # Payment signature verification failed
       # Handle the error accordingly
       return render(request, 'payment_failure.html')


import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from .models import ContactFormSubmission

@login_required(login_url="/auth/login") 
def contact_form_submission(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        selected_car_id = request.POST.get('selected_car') # Extract selected car ID from the form data
        selected_car = None
        if selected_car_id:
            selected_car = Car.objects.get(pk=selected_car_id)  
        
        # Save data to database
        contact_submission = ContactFormSubmission.objects.create(name=name, phone=phone, email=email, message=message,selected_car=selected_car)
        
        
        
        return HttpResponse('Submitted successfully and sent to API')
       
    else:  
        return redirect('home')
       
       
        
       


        # Return an error response for unsupported methods
        

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ContactFormSubmission
from .serializers import ContactFormSubmissionSerializer
from .serializers import LoanApplicationSerializer




class ContactFormSubmission1View(APIView):
  serializer_class=LoanApplicationSerializer
  
  
  
  def get_queryset(self):
      contacts=LoanApplication.objects.all()
      return contacts
      
      
  
   
  def get(self, request):
        submissions = ContactFormSubmission.objects.all()
        serializer = ContactFormSubmissionSerializer(submissions, many=True)
        return Response(serializer.data)
   
  
       
  def post(self, request):
        

            
           
            serializer = LoanApplicationSerializer(data=request.data)
            
            if serializer.is_valid():
                # Save the data
                serializer.save()
                loan_application_data = serializer.data
                # Return success response
                return Response(serializer.data, status=rest_framework_status.HTTP_201_CREATED)
            else:
                # Return error response if data is not valid
                return Response(serializer.errors,  status=rest_framework_status.HTTP_400_BAD_REQUEST)
        
  def delete(request, self):
     submissions = ContactFormSubmission.objects.all()
     submissions.delete()
     return Response(status=rest_framework_status.HTTP_202_ACCEPTED)


# views.py

from django.shortcuts import render, redirect
from .models import Car





def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, 'car_detail.html', {'car': car})


def purchase_car(request, car_id):
    # Logic to handle purchasing a car
    return render(request, 'purchase_car.html')


@login_required(login_url="/auth/login") 
def add_to_wishlist(request, car_id):
    car = Car.objects.get(pk=car_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.cars.add(car)
    return redirect('wishlist')

@login_required(login_url="/auth/login") 
def remove_from_wishlist(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.cars.remove(car)
    return JsonResponse({'success': True})

@login_required(login_url="/auth/login") 
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_car_ids = wishlist.cars.values_list('id', flat=True)
    return render(request, 'wishlist.html', {'wishlist_cars': wishlist.cars.all(),})

@login_required(login_url="/auth/login") 
def user_history(request):
    user = request.user
    
    # Fetch user-specific data for different services
    service_bookings = ServiceBooking.objects.filter(customer_name=user.username)
    test_drives = TestDrive.objects.filter(customer_name=user.username)
    loan_applications = LoanApplication.objects.filter(name=user.username)
    
    return render(request, 'user_history.html', {'service_bookings': service_bookings, 'test_drives': test_drives, 'loan_applications': loan_applications})






