from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.models import LogEntry
from .models import CustomUser

admin.site.register(CustomUser, UserAdmin)

# Update the LogEntry model to use your custom user model
from django.contrib.auth import get_user_model

CustomUserModel = get_user_model()

LogEntry._meta.get_field('user').related_model = CustomUserModel

# admin.py

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

class FinancierAdminSite(admin.AdminSite):
    site_header = 'Financier Administration'
    site_title = 'Financier Admin'

    def each_context(self, request):
        context = super().each_context(request)
        context['financier_dashboard_url'] = reverse('financier_dashboard')
        return context

admin_site = FinancierAdminSite(name='financier_admin')
