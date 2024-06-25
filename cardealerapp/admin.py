from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.contrib import admin
from .models import Car, ServiceBooking, TestDrive, Financier, Wishlist, Wishlist_Car, ContactFormSubmission, LoanApplication, Reservation, Order
from django.http import HttpRequest, HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import letter
from django import forms
from django.shortcuts import render
from django.contrib.admin import DateFieldListFilter



@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['car_name', 'category', 'price', 'make', 'model','display_image', 'year', 'transmission_type', 'description']
    list_filter = ['category', 'make', 'year', 'transmission_type']  
    

@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'car', 'service_type', 'date', 'time', 'location', 'address', 'created_at', 'comments']
    list_filter = ['service_type', 'location', 'status',('date', DateFieldListFilter)]  # Add filters for service type, location, and status
   
    
    
    def generate_pdf_report(self, request, queryset):
        # Get the selected service bookings from the queryset
        selected_service_bookings = queryset

        # Generate PDF report
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="service_booking_report.pdf"'

        # Create PDF document
        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []

        # Table data
        data = [[ 'Customer', 'Car', 'Service Type', 'Date','Location',]]
        for service_booking in selected_service_bookings:
            data.append([ service_booking.customer_name, service_booking.car, service_booking.service_type, service_booking.date, service_booking.location, service_booking.status])

        # Create table
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        elements.append(table)
        doc.build(elements)
        return response

    generate_pdf_report.short_description = "Generate PDF Report"
    actions = ['generate_pdf_report']


@admin.register(TestDrive)
class TestDriveAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'car', 'date', 'time', 'location', 'address', 'created_at']
    list_filter = ['location', 'status',('date', DateFieldListFilter)]  # Add filters for location and status
   
    
    
    
    
    def generate_pdf_report(self, request, queryset):
        # Get the selected test drives from the queryset
        selected_test_drives = queryset

        # Generate PDF report
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="test_drive_report.pdf"'

        # Create PDF document
        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []

        # Table data
        data = [['Test Drive ID', 'Customer', 'Car', 'Date', 'Time', 'Location']]
        for test_drive in selected_test_drives:
            data.append([test_drive.id, test_drive.customer_name, test_drive.car, test_drive.date, test_drive.time, test_drive.location,])

        # Create table
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        elements.append(table)
        doc.build(elements)
        return response

    generate_pdf_report.short_description = "Generate PDF Report"
    actions = ['generate_pdf_report']

@admin.register(Financier)
class FinancierAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_name', 'email', 'contact_number', 'website',]
   
    list_filter = ['name', 'company_name']  
@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'selected_car', 'message', 'created_at']
   
    list_filter = ['name', 'email','selected_car__car_name']
    def active(self,obj):
        return obj.is_active == 1
    active.boolean= True
    
    def has_add_permission(self, request):
        return False
@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'selected_car', 'message', 'status', 'created_at']
    list_filter = ['status']  # Add filter for status
   
    def active(self,obj):
        return obj.is_active == 1
    active.boolean= True
    
    def has_add_permission(self, request):
        return False
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['token_id','user', 'car','reservation_date', 'expiration_date', 'token_amount', 'is_active']
    list_filter = ['status', 'is_active', ('reservation_date', DateFieldListFilter)]  # Add filters for status and is_active
   
    def active(self,obj):
        return obj.is_active == 1
    active.boolean= True
    
    def has_add_permission(self, request):
        return False
    
    def generate_pdf_report(self, request, queryset):
        # Get the selected reservations from the queryset
        selected_reservations = queryset

        # Generate PDF report
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reservation_report.pdf"'

        # Create PDF document
        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []

        # Table data
        data = [['Reservation ID', 'User', 'Car', 'Reservation Date']]
        for reservation in selected_reservations:
            data.append([reservation.token_id, reservation.user.username, reservation.car, reservation.reservation_date])

        # Create table
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        elements.append(table)
        doc.build(elements)
        return response

    generate_pdf_report.short_description = "Generate PDF Report"
    actions = ['generate_pdf_report']



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'car', 'order_date', 'delivery_date', 'delivery_location', 'price', 'payment_status', 'order_status', 'additional_information', 'reservation']
    list_filter = ['payment_status', 'order_status', ('order_date', admin.DateFieldListFilter)]  # Date hierarchy filter
   
    def generate_pdf_report(self, request, queryset):
        # Get the selected orders from the queryset
        selected_orders = queryset

        # Generate PDF report
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="order_report.pdf"'

        # Create PDF document
        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []

        # Table data
        data = [['Order ID', 'Customer', 'Car', 'Order Date', 'Delivery Date']]
        for order in selected_orders:
            data.append([order.order_id, order.user.username, order.car, order.order_date, order.delivery_date])

        # Create table
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        elements.append(table)
        doc.build(elements)
        return response

    generate_pdf_report.short_description = "Generate PDF Report"
    actions = ['generate_pdf_report']

