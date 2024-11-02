from django.contrib import admin

from .models import Visit


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_id', 'doctor_id', 'date', 'is_deleted')
    list_filter = ('is_deleted',)
