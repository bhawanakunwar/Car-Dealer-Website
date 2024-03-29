from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.models import LogEntry
from .models import CustomUser



# Update the LogEntry model to use your custom user model
from django.contrib.auth import get_user_model

CustomUserModel = get_user_model()

LogEntry._meta.get_field('user').related_model = CustomUserModel

# admin.py

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'mob_number')  # Removed 'is_email_verified'
    list_filter = ('is_staff', 'is_superuser', 'groups', 'user_permissions')
    search_fields = ('email', 'username', 'mob_number')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)