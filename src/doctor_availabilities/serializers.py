from rest_framework import serializers
from .models import DoctorAvailability


class DoctorAvailabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorAvailability
        fields = ['doctor_id', 'date', 'available_hours', 'price']
