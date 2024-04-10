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
from django.contrib import messages


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
        
        customer_name = request.user.username 
        location = request.POST.get('location')
        address = request.POST.get('address', '') # Address might not be present if location is 'center'
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.strptime(time_str, '%H').time() 

        test_drive = TestDrive(
            car_id=car_id,
            customer_name=customer_name,
            location=location,
            address=address,
            date=date,
            time=time
        )
        current_datetime = datetime.now()
        if date < current_datetime.date() or (date == current_datetime.date() and time < current_datetime.time()):
            test_drive.status = "Completed"
        elif date == current_datetime.date() and time == current_datetime.time():
            test_drive.status = "Pending"
        else:
            test_drive.status = "Pending"
        
        test_drive.save()

        # Return a JSON response indicating success
        messages.success(request,"Test Drive Booked Successfully")
        return redirect('user_history')
    else:
        # Handle GET requests for the form here if needed
        available_cars = Car.objects.all()  # Fetch available cars from the database
       
        
        return render(request, 'book_test_drive.html', {'available_cars': available_cars,'username': request.user.username})

    

  


@login_required(login_url="/auth/login") 
def book_test_drive_from_car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    
    if request.method == 'POST':
    
        customer_name = request.user.username 
        location = request.POST.get('location')
        address = request.POST.get('address', '') # Address might not be present if location is 'center'
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.strptime(time_str, '%H').time() 

       

        # Save the form data to the database
        test_drive = TestDrive(
            car=car,
            customer_name=customer_name,
            location=location,
            address=address,
            date=date,
            time=time
        )
        current_datetime = datetime.now()
        if date < current_datetime.date() or (date == current_datetime.date() and time < current_datetime.time()):
            test_drive.status = "Completed"
        elif date == current_datetime.date() and time == current_datetime.time():
            test_drive.status = "Pending"
        else:
            test_drive.status = "Pending"
        
        test_drive.save()

        # Return a JSON response indicating success
        messages.success(request,"Test Drive Booked Successfully")
        return redirect('user_history')
    else:
        
        available_cars = Car.objects.all()  # Fetch available cars from the database
     
        
        return render(request, 'book_test_drive.html', {'car':car,'available_cars': available_cars,'username': request.user.username})





@login_required(login_url="/auth/login")     
def test_drive_success(request):
    return render(request, 'test_drive_success.html')
@login_required(login_url="/auth/login") 
def book_service(request,car_id=None):
    if request.method == 'POST':
        # Retrieve form data
        car_name = request.POST.get('car')
        car = get_object_or_404(Car, car_name=car_name)
        customer_name = request.user.username  
        location = request.POST.get('location')
        address = request.POST.get('address', '')  # Address might not be present if location is 'center'
        service_type = request.POST.get('service_type')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.strptime(time_str, '%H').time() 

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

        current_datetime = datetime.now()
        if date < current_datetime.date() or (date == current_datetime.date() and time < current_datetime.time()):
            service_booking.status = "In Progress"
        elif date == current_datetime.date() and time == current_datetime.time():
            service_booking.status = "Pending"
        else:
             service_booking.status = "Pending"
        
        service_booking.save()

        messages.success(request,"Service Booked Successfully")
        return redirect('user_history')
        
    else:
        # Handle GET requests for the form here if needed
       ordered_cars = Car.objects.filter(order__user=request.user)
       return render(request, 'book_service.html', {'ordered_cars': ordered_cars,'username': request.user.username})
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
from cardealer.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY

client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))

@login_required(login_url="/auth/login") 
def checkout(request, car_id):
    selected_car = None
    if car_id:
        selected_car = Car.objects.get(pk=car_id)

    financiers = Financier.objects.all()[:3]
    available_cars = Car.objects.all()  

    # Razorpay setup
    order_amount = 200000
    order_currency = 'INR'

    user = request.user
    username = user.username
    email = user.email
    mob_number = user.mob_number 

    # Create Razorpay payment order
    payment_order = client.order.create(dict(amount=order_amount, currency=order_currency, payment_capture=1))
    payment_order_id = payment_order['id']

    context = {
        'selected_car': selected_car,
        'financiers': financiers,
        'available_cars': available_cars,
        'amount': 2000,
        'api_key': RAZORPAY_API_KEY,
        'order_id': payment_order_id,'username': username,
        'email': email,
        'mob_number': mob_number
    }
    
    # Pass context to the template
    return render(request, 'checkout.html', context)
from .models import Reservation
import uuid
from datetime import datetime, timedelta
from django.urls import reverse
import random
import string

@login_required(login_url="/auth/login") 
def payment_success(request):
    if request.method == 'POST':
        # Handle payment success
        order_id = request.POST.get('razorpay_order_id')
        payment_id = request.POST.get('razorpay_payment_id')
        
        # Generate a unique token ID
        token_id = f"#{''.join(random.choices(string.digits, k=6))}"
        
        # Assuming user and car details are available in the request or can be fetched
        user = request.user  # Assuming user is authenticated
        car_id = request.POST.get('car_id')  # Assuming you're passing car_id in the request
        
        # Retrieve the car object
        car = Car.objects.get(pk=car_id)
        current_datetime = timezone.now()
        expiration_datetime = current_datetime + timedelta(days=7)  # Assuming 7 days validity
        
        # Check if the reservation is expired
        if expiration_datetime < current_datetime:
            status = 'expired'
        else:
            status = 'valid'
        # Create a new Reservation with the payment and order IDs
        reservation = Reservation.objects.create(
            user=user,
            car=car,
            reservation_date=timezone.now(),
            expiration_date=timezone.now() + timedelta(days=7),  # Adjust expiration date as needed
            token_amount=2000,  # Assuming a fixed token amount, you can adjust this as needed
            is_active=True,
            order_id=order_id,
            payment_id=payment_id,
            token_id=token_id,
            status=status 
        )
        
        messages.success(request,"Payment Successful! Token generated.")
        return redirect(reverse('checkout', kwargs={'car_id': car_id}))
    else:
        messages.error(request,"Invalid Request")
        return redirect('checkout') 

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from .models import ContactFormSubmission

@login_required(login_url="/auth/login") 
def contact_form_submission(request):
    if request.method == 'POST':
    
        # Get user's details
        user = request.user
        name = user.username
        email = user.email
        phone = user.mob_number
        message = request.POST.get('message')
        selected_car_id = request.POST.get('selected_car') # Extract selected car ID from the form data
        selected_car = None
        if selected_car_id:
            selected_car = Car.objects.get(pk=selected_car_id)  
        
        # Save data to database
        contact_submission = ContactFormSubmission.objects.create(name=name, phone=phone, email=email, message=message,selected_car=selected_car)
        
        
        
        messages.success(request,"Form Submitted successfully")
        return redirect('checkout', car_id=selected_car_id)  
    else:  
           messages.error(request, "Failed to submit form")
           return redirect('checkout', car_id=selected_car_id) 
       
        
       


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
    current_user = request.user
    has_booked_test_drive = TestDrive.objects.filter(car=car, customer_name=current_user.username, date=timezone.now().date(), time__gte=timezone.now().strftime('%H:%M')).exists()
    context = {
        'car': car,
        'has_booked_test_drive': has_booked_test_drive
    }
    return render(request, 'car_detail.html', context)


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
from .models import Order
from datetime import datetime, date
@login_required(login_url="/auth/login") 
def user_history(request):
    user = request.user
    
    # Fetch user-specific data for different services
    service_bookings = ServiceBooking.objects.filter(customer_name=user.username)
    test_drives = TestDrive.objects.filter(customer_name=user.username)
    loan_applications = LoanApplication.objects.filter(name=user.username)
    reservations = Reservation.objects.filter(user=user)
    orders = Order.objects.filter(user=user) 
    
    
    current_date = date.today()
    current_time = datetime.now().time()
    
    for test_drive in test_drives:
        start_time = datetime.combine(test_drive.date, test_drive.time)
        end_time = (start_time + timedelta(hours=1)).time()
        if current_date > test_drive.date or (current_date == test_drive.date and current_time > start_time.time()):
            test_drive.status = "Completed"
        else:
            test_drive.status = "Pending"
    
    for service_booking in service_bookings:
        start_time = datetime.combine(service_booking.date, service_booking.time)
        end_time = (start_time + timedelta(hours=1)).time()
        if current_date > service_booking.date or (current_date == service_booking.date and current_time > start_time.time()):
            service_booking.status = "In Progress"
        else:
            service_booking.status = "Pending"


   
    for reservation in reservations:
        expiration_datetime = reservation.expiration_date
        if expiration_datetime.date() < current_date:
            reservation.status = "Expired"
        else:
            reservation.status = "Valid"
    return render(request, 'user_history.html', {'service_bookings': service_bookings, 'test_drives': test_drives, 'loan_applications': loan_applications, 'reservations': reservations, 'orders': orders, 'current_date': current_date, 'current_time': current_time})

def cancel_service_booking(request, booking_id):
    # Get the service booking object
    service_booking = get_object_or_404(ServiceBooking, id=booking_id)
    
    # Check if the booking belongs to the current user (optional)
    if service_booking.customer_name != request.user.username:
        # You can customize the error message based on your preference
        messages.error(request, "You are not authorized to cancel this booking.")
        return redirect('user_history')
    
    # Perform cancellation logic here (e.g., delete the booking)
    service_booking.status = "Cancelled"
    service_booking.save()
    
    # Redirect back to the user history page
    return redirect('user_history')


def cancel_test_drive(request, booking_id):
    # Get the test drive object
    test_drive = get_object_or_404(TestDrive, id=booking_id)
    
    # Check if the booking belongs to the current user (optional)
    if test_drive.customer_name != request.user.username:
        # You can customize the error message based on your preference
        messages.error(request, "You are not authorized to cancel this booking.")
        return redirect('user_history')
    test_drive.status = "Cancelled"
    test_drive.save()
    
    return redirect('user_history')