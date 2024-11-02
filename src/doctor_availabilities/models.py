from django.db import models


class DoctorAvailability(models.Model):
    doctor_id = models.IntegerField()
    date = models.DateField()
    available_hours = models.JSONField()  # Przechowuje godziny i ich dostępność
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def set_availability(self, hours):
        # Ustawienie początkowej dostępności godzin (np. {'8': True, '9': True, '10': True})
        self.available_hours = {str(hour): True for hour in hours}
        self.save()

    def mark_as_booked(self, hour):
        # Oznaczenie konkretnej godziny jako zarezerwowanej
        if self.available_hours.get(str(hour)) is not None:
            self.available_hours[str(hour)] = False
            self.save()

    def is_hour_available(self, hour):
        # Sprawdzenie, czy konkretna godzina jest dostępna
        return self.available_hours.get(str(hour), False)
