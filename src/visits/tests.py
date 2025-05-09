from decimal import Decimal

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Visit
from .serializers import VisitSerializer
from .factory_models import VisitFactory
from core.settings import HTTP_URL

from responses import activate, add


class TestVisitsView(APITestCase):
    def setUp(self) -> None:
        self.visit_url = reverse('visit-list')

        self.visit_data = {
            "patient_id": 11,
            "doctor_id": 2,
            "date": "2024-12-01T11:00:00+01:00",
            "patient_email": "test@example.com",
            "price": Decimal(100),
            "title": "Wizyta kontrolna"
        }
        self.visit = VisitFactory(patient_id=1, doctor_id=2)

    def test_get_visit_details(self):
        response = self.client.get(reverse('visit-detail', args=[self.visit.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, VisitSerializer(self.visit).data)

    @activate
    def test_create_visit(self):
        add(
            method='GET',
            url=f"{HTTP_URL}/users/11/",
            json={"id": 11, "role": "Patient"},
            status=200
        )
        add(
            method='GET',
            url=f"{HTTP_URL}/users/2/",
            json={"id": 2, "role": "Doctor"},
            status=200
        )
        response = self.client.post(self.visit_url, data=self.visit_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["patient_id"], 11)
        self.assertEqual(Visit.objects.filter(patient_id=11).count(), 1)

    @activate
    def test_create_doctor_not_found(self):
        add(
            method='GET',
            url=f"{HTTP_URL}/users/11/",
            json={"id": 11, "role": "Patient"},
            status=200
        )
        add(
            method='GET',
            url=f"{HTTP_URL}/users/2/",
            status=404
        )
        response = self.client.post(self.visit_url, data=self.visit_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Doctor not found.', response.data["message"])

    @activate
    def test_create_patient_not_found(self):
        add(
            method='GET',
            url=f"{HTTP_URL}/users/11/",
            status=404
        )
        add(
            method='GET',
            url=f"{HTTP_URL}/users/2/",
            json={"id": 2, "role": "Doctor"},
            status=200
        )
        response = self.client.post(self.visit_url, data=self.visit_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Patient not found.', response.data["message"])

    def test_get_patient_visits(self):
        VisitFactory(patient_id=1, doctor_id=2)

        response = self.client.get(reverse('visit-get-patient-visits', args=[1]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Visit.objects.filter(patient_id=1).count(), len(response.data))

    def test_soft_delete_visit_success(self):
        response = self.client.delete(
                reverse('visit-soft-delete-visit', args=[self.visit.id]),
                HTTP_AUTHORIZATION='Bearer mocktoken',
                HTTP_ROLE='Doctor'
            )
        self.assertFalse(self.visit.is_deleted)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.visit.refresh_from_db()
        self.assertTrue(self.visit.is_deleted)

    def test_soft_delete_already_deleted_visit(self):
        self.visit.soft_deleted()
        self.visit.refresh_from_db()

        response = self.client.delete(
                reverse('visit-soft-delete-visit', args=[self.visit.id]),
                HTTP_AUTHORIZATION='Bearer mocktoken',
                HTTP_ROLE='Doctor'
            )

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("That visit was deleted.", response.data["message"])

    def test_soft_delete_visit_by_patient(self):
        response = self.client.delete(
                reverse('visit-soft-delete-visit', args=[self.visit.id]),
                HTTP_AUTHORIZATION='Bearer mocktoken',
                HTTP_ROLE='Patient'
            )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('Only doctors can delete visit.', response.data["message"])
