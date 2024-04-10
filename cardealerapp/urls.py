from django.urls import path
from cardealerapp import views

# In urls.py
from .serializers import ContactFormSubmissionSerializer






urlpatterns=[
  path('index',views.index,name="index"),  
  path('search/',views.search,name='search'),
  path('test_drive_success/', views.test_drive_success, name='test_drive_success'),
  path('book_service/', views.book_service, name='book_service'),
 
  path('cars/', views.car_list, name='car_list'),
  path('user-history/',views.user_history, name='user_history'),
  
  path('checkout/<int:car_id>/', views.checkout, name='checkout'),
  path('payment_success/',views.payment_success,name='payment_success'),
  
  path('add-to-wishlist/<int:car_id>/', views.add_to_wishlist, name='add_to_wishlist'),
  path('remove-from-wishlist/<int:car_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
  path('wishlist/', views.wishlist, name='wishlist'),
  path('contact_form_submission/', views.contact_form_submission, name='contact_form_submission'),
  path('car/<int:car_id>/', views.car_detail, name='car_detail'),
  path('purchase_car/<int:car_id>/', views.purchase_car, name='purchase_car'),
  path('financiers/', views.ContactFormSubmission1View.as_view(), name='financiers'), 
  
  path('book_test_drive/', views.book_test_drive, name='book_test_drive'),
 
  path('book_test_drive_from_car_detail/<int:car_id>/', views.book_test_drive_from_car_detail, name='book_test_drive_from_car_detail'),
  path('cancel/service_booking/<int:booking_id>/', views.cancel_service_booking, name='cancel_service_booking'),
   path('cancel/test_drive/<int:booking_id>/', views.cancel_test_drive, name='cancel_test_drive'),  
]




