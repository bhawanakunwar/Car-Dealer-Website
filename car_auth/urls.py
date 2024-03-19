# car_auth/urls.py

from django.urls import path
from .views import signup, handlelogin,handlelogout,my_account
app_name = 'car_auth'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', handlelogin, name='handlelogin'),
    path('logout/', handlelogout, name='handlelogout'),
    path('my-account/', my_account, name='my_account'),
]
