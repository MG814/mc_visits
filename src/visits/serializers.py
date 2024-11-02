from rest_framework import serializers
from .models import Visit


class VisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visit
        fields = ['patient_id', 'doctor_id', 'date', 'title']
