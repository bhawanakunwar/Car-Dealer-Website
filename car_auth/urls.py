# car_auth/urls.py

from django.urls import path
from .views import signup, handlelogin,handlelogout,my_account,edit_profile,change_password
app_name = 'car_auth'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', handlelogin, name='handlelogin'),
    path('logout/', handlelogout, name='handlelogout'),
    path('edit-profile/', edit_profile, name='edit_profile'),
      path('change-password/', change_password, name='change_password'), 
    path('my-account/', my_account, name='my_account'),
]
