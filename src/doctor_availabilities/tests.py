from decimal import Decimal

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import DoctorAvailability
from .serializers import DoctorAvailabilitySerializer
from .factory_models import DoctorAvailabilityFactory
from core.settings import HTTP_URL

from responses import activate, add
import json


class TestDoctorAvailabilityView(APITestCase):
    def setUp(self) -> None:
        self.availability_url = reverse('availability-list')

        self.doctor_availability_data = {
            "doctor_id": 2,
            "date": "2024-10-26",
            "available_hours": json.dumps({
                "8": True,
                "9": True,
                "10": False
            }),
            "price": "100.00"
        }
        self.doctor_availability = DoctorAvailabilityFactory(doctor_id=2)

    def test_get_doctor_availability_list(self):
        DoctorAvailabilityFactory.create_batch(5)

        response = self.client.get(reverse('availability-get-doctor-availability', args=[2]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DoctorAvailability.objects.filter(doctor_id=2).count(), len(response.data))

    def test_get_doctor_availability_details(self):
        response = self.client.get(reverse('availability-detail', args=[self.doctor_availability.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, DoctorAvailabilitySerializer(self.doctor_availability).data)

    @activate
    def test_create_availability_success(self):
        add(
            method='GET',
            url=f"{HTTP_URL}/users/2/",
            json={"id": 2, "role": "Doctor"},
            status=200
        )
        response = self.client.post(self.availability_url, data=self.doctor_availability_data,
                                    HTTP_AUTHORIZATION='Bearer mocktoken',
                                    HTTP_ROLE='Doctor')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["doctor_id"], 2)
        self.assertEqual(DoctorAvailability.objects.filter(doctor_id=2).count(), 2)

    @activate
    def test_create_availability_doctor_not_found(self):
        add(
            method='GET',
            url=f"{HTTP_URL}/users/2/",
            json={"id": 2, "role": "Doctor"},
            status=404
        )
        response = self.client.post(self.availability_url, data=self.doctor_availability_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Doctor not found.', response.data["message"])

    @activate
    def test_create_availability_by_patient(self):
        add(
            method='GET',
            url=f"{HTTP_URL}/users/2/",
            json={"id": 2, "role": "Patient"},
            status=200
        )
        response = self.client.post(self.availability_url, data=self.doctor_availability_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('Only doctors can create this.', response.data["message"])

    def test_get_doctor_availability_update(self):
        updated_data = {
            "price": "150.00",
            "available_hours": json.dumps({
                "11": False,
                "12": True,
                "13": False
            })
        }
        response = self.client.patch(reverse('availability-detail', args=[self.doctor_availability.id]),
                                     data=updated_data)
        self.doctor_availability.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.doctor_availability.price, Decimal("150.00"))
        self.assertEqual(json.dumps(self.doctor_availability.available_hours), updated_data["available_hours"])


