from django.contrib import admin
from .models import Car, ServiceBooking, TestDrive, Financier, Wishlist, Wishlist_Car, ContactFormSubmission, LoanApplication, Reservation, Order

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['car_name', 'category', 'price', 'make', 'model','display_image', 'year', 'transmission_type', 'description']


@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'car', 'service_type', 'date', 'time', 'location', 'address', 'created_at', 'comments']

@admin.register(TestDrive)
class TestDriveAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'car', 'date', 'time', 'location', 'address', 'created_at']

@admin.register(Financier)
class FinancierAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_name', 'email', 'contact_number', 'website',]

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user']

@admin.register(Wishlist_Car)
class Wishlist_CarAdmin(admin.ModelAdmin):
    list_display = ['wishlist', 'car']

@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'selected_car', 'message', 'created_at']

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'selected_car', 'message', 'status', 'created_at']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'reservation_date', 'expiration_date', 'token_amount', 'is_active']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'car', 'order_date', 'delivery_date', 'delivery_location', 'price', 'payment_status', 'order_status', 'additional_information', 'reservation']
