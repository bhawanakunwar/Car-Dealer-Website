from django.contrib import admin

# Register your models here.
from .models import TestDrive,ServiceBooking,Car,Financier,Wishlist,ContactFormSubmission,Order

admin.site.register(TestDrive)
admin.site.register(ServiceBooking)
admin.site.register(Car)
admin.site.register(Financier)
admin.site.register(Wishlist)
admin.site.register(Order)


@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone', 'message')

from django.contrib import admin
from .models import LoanApplication

class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')

admin.site.register(LoanApplication ,LoanApplicationAdmin)

