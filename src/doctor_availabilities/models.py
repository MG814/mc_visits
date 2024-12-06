from django.db import models


class DoctorAvailability(models.Model):
    doctor_id = models.IntegerField()
    date = models.DateField()
    available_hours = models.JSONField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
