from django.contrib import admin

# Import app-specific admin configurations
from cardealerapp import admin as cardealerapp_admin
from car_auth import admin as car_auth_admin

# Include app-specific admin configurations
admin.site = cardealerapp_admin
admin.site = car_auth_admin
