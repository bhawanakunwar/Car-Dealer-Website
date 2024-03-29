
print("This is a test message")


# views.py in your app
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate,get_user_model
from django.contrib import messages
from car_auth import models
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from .tokens import generate_token
import re


User = get_user_model()#Create your views here.
def signup(request):
    print("view accessed")
    if request.method == "POST":
        # If the form is submitted via POST, extract the data from the request
        username = request.POST.get('username')
        email = request.POST.get('email')
        mob_number = request.POST.get('mob_number')
        password = request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        
       
        if not (username and email and mob_number and password and confirm_password):
            messages.error(request, "All fields must be filled out")
            return render(request, 'authentication/signup.html')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'authentication/signup.html')
        
        if not re.match(r'\S+@\S+\.\S+', email):
            messages.error(request, "Invalid email address")
            return render(request, 'authentication/signup.html')
        
        if not re.match(r'^[0-9]{10}$', mob_number):
            messages.error(request, "Invalid phone number. Phone number must be 10 digits")
            return render(request, 'authentication/signup.html')
        
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            return render(request, 'authentication/signup.html')
         
       
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists! Please try a different email.")
            return render(request, 'authentication/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try a different username.")
            return render(request, 'authentication/signup.html')
        if User.objects.filter(mob_number=mob_number).exists():
            messages.error(request, "Mobile number already exists! Please try a different number.")
            return render(request, 'authentication/signup.html')
    
        new_user = User.objects.create_user(username, email, password=password, mob_number=mob_number)
        new_user.is_active=True

        new_user.save()
        messages.success(request,'successfully Registered,Please Login')
        return redirect('/auth/login')
    
    return render(request, "authentication/signup.html")

           
    

def handlelogin(request):
    

    if request.method=="POST":
        
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        if not (email and password):
            messages.error(request, "Email and password are required.")
            return render(request, 'authentication/login.html')
        
        user=authenticate(request,email=email,password=password)

        


        if user is not None:
            login(request,user)
            return redirect("/index")
        else:
            messages.error(request,"Email and password do not match ")
            return redirect('/auth/login')      

        


    
    return render (request,"authentication/login.html")
def handlelogout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    # Redirect to the home page or any other page after logout
    return render(request,"authentication/myaccount.html")

def my_account(request):
    return render(request, "authentication/myaccount.html")




