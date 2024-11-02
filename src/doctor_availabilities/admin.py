from django.contrib import admin

from .models import DoctorAvailability


@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor_id', 'date', 'available_hours')
