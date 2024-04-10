
print("This is a test message")


# views.py in your app
from django.contrib.auth import update_session_auth_hash
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

def edit_profile(request):
    if request.method == 'POST':
        # Extract the data from the request
        username = request.POST.get('username')
        email = request.POST.get('email')
        mob_number = request.POST.get('mob_number')
        
        # Validate the data
        if not (username and email and mob_number):
            messages.error(request, "All fields must be filled out")
            return redirect('edit_profile')  # Redirect back to the edit profile page
            
        if not re.match(r'\S+@\S+\.\S+', email):
            messages.error(request, "Invalid email address")
            return redirect('edit_profile')  # Redirect back to the edit profile page
        
        if not re.match(r'^[0-9]{10}$', mob_number):
            messages.error(request, "Invalid phone number. Phone number must be 10 digits")
            return redirect('edit_profile')  # Redirect back to the edit profile page
        
        # Check if the email is already in use by another user
        if User.objects.filter(email=email).exclude(id=request.user.id).exists():
            messages.error(request, "Email already exists! Please try a different email.")
            return redirect('edit_profile')  # Redirect back to the edit profile page
        
        # Check if the username is already in use by another user
        if User.objects.filter(username=username).exclude(id=request.user.id).exists():
            messages.error(request, "Username already exists! Please try a different username.")
            return redirect('edit_profile')  # Redirect back to the edit profile page
        
        # Update the user's profile
        user = request.user
        user.username = username
        user.email = email
        user.mob_number = mob_number
        user.save()
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('car_auth:edit_profile')
    
    return render(request, 'authentication/edit_profile.html')

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

           
def change_password(request):
    if request.method == 'POST':
        # Extract the data from the request
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        # Check if current password matches
        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('car_auth:change_password')
        
        # Check if new password matches confirm password
        if new_password != confirm_new_password:
            messages.error(request, "New password and confirm password do not match.")
            return redirect('car_auth:change_password')

        # Check if new password is different from current password
        if current_password == new_password:
            messages.error(request, "New password must be different from current password.")
            return redirect('car_auth:change_password')

        # Update the user's password
        user = request.user
        user.set_password(new_password)
        user.save()

        # Update the session auth hash
        update_session_auth_hash(request, user)

        messages.success(request, "Your password has been changed successfully.")
        return redirect('car_auth:change_password')

    return render(request, 'authentication/change_password.html')   

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




