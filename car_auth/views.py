
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
        
        if User.objects.filter(username=username).exists():
         messages.error(request, "Username already exists! Please try a different username.")
         return render(request,'authentication/signup.html')
        
        
        if password!=confirm_password:
             return render(request, 'authentication/signup.html', {'error': 'Passwords do not match'})
        try:
            if User.objects.get(username=email):
                 return render(request, 'authentication/signup.html', {'error': 'Username already exists'})
        except Exception as identifier:
            pass
        
           

        # Create a new user
        new_user = User.objects.create_user(username, email, password=password, mob_number=mob_number)
        new_user.is_active=False

        new_user.save()
        # Send welcome email
        subject = "Welcome to Our Django User Registration System"
        message = f"Hello {new_user.username}!\n\nThank you for registering on our website. Please confirm your email address to activate your account.\n\nRegards,\nThe Django Team"
        from_email = settings.EMAIL_HOST_USER
        to_list = [new_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
# Send email confirmation link
        current_site = get_current_site(request)
        email_subject = "Confirm Your Email Address"
        message2 = render_to_string('authentication/email_confirmation.html', {
       'name': new_user.username,
       'domain': current_site.domain,
       'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
        'token': generate_token.make_token(new_user)
 })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [new_user.email],
  )
        send_mail(email_subject, message2, from_email, to_list, fail_silently=True)
        messages.success(request, "Your account has been created successfully! Please check your email to confirm your email address and activate your account.")
        return redirect('auth/login')
    return render(request, "authentication/signup.html")

           
    
    return render(request,"authentication/signup.html")
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        new_user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
      new_user = None

    if new_user is not None and generate_token.check_token(new_user, token):
     new_user.is_active = True
     new_user.save()
     login(request, new_user)
     messages.success(request, "Your account has been activated!")
     return redirect('signin')
    else:
     return render(request, 'activation_failed.html')

# views.py


def handlelogin(request):
    

    if request.method=="POST":
        
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(f"Email: {email}")
        print(f"Password: {password}")

        user=authenticate(request,email=email,password=password)

        


        if user is not None:
            login(request,user)
            if request.GET.get('next',None):
                return HttpResponseRedirect(request.GET['next'])

            messages.success(request,"Login Success")
            return redirect("/")
        else:
            messages.error(request,"invalid credentials")
            return redirect('/auth/login')      

        


    
    return render (request,"authentication/login.html")
def handlelogout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    # Redirect to the home page or any other page after logout
    return render(request,"authentication/myaccount.html")

def my_account(request):
    return render(request, "authentication/myaccount.html")




