from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.models import LogEntry
from .models import CustomUser
from django.contrib.admin import DateFieldListFilter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import letter
from django import forms
from django.shortcuts import render
from django.contrib.admin import DateFieldListFilter
from django.http import HttpResponse

admin.site.site_header ="Login Carzone"
admin.site.index_title="Welcome To Carzone's Dashboard"

# Update the LogEntry model to use your custom user model
from django.contrib.auth import get_user_model

CustomUserModel = get_user_model()

LogEntry._meta.get_field('user').related_model = CustomUserModel

# admin.py

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = ('email', 'username', 'mob_number','date_joined')  # Removed 'is_email_verified'
    list_filter = ('is_staff',  ('date_joined', DateFieldListFilter))
    
    ordering = ('username',)
    def active(self,obj):
        return obj.is_active == 1
    active.boolean= True
    
    def has_add_permission(self, request):
        return False
    
    def generate_pdf_report(self, request, queryset):
        # Get the selected service bookings from the queryset
        selected_custom_users = queryset

        # Generate PDF report
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="service_booking_report.pdf"'

        # Create PDF document
        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []

        # Table data
        data = [[ 'Customer','Email', 'Mobile number','date_joined']]
        for user in selected_custom_users:
            data.append([user.username,user.email,user.mob_number,user.date_joined])

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



