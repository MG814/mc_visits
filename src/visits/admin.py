from django.contrib import admin

from .models import Visit


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_id', 'doctor_id', 'date', 'price', 'is_deleted', 'is_paid')
    list_filter = ('is_deleted', 'is_paid')
