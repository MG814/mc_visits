import requests
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.decorators import action

from doctor_availabilities.models import DoctorAvailability
from doctor_availabilities.serializers import DoctorAvailabilitySerializer


class DoctorAvailabilityView(GenericViewSet, UpdateModelMixin, ListModelMixin, RetrieveModelMixin):
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [AllowAny]

    @action(methods=['GET'], detail=False, url_path='doctors/(?P<doctor_id>\d+)')
    def get_doctor_availability(self, request, doctor_id=None):
        queryset = self.get_queryset().filter(doctor_id=doctor_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_user_role = self.request.headers.get('role')

        token = self.request.headers.get('Authorization')
        accounts_service_url = 'http://web-accounts:8100/users/'

        headers = {
            'Authorization': token
        }

        doctor_id = self.request.data.get('doctor_id')
        doctor_url = f'{accounts_service_url}{doctor_id}/'

        doctor_response = requests.get(doctor_url, headers=headers)

        if doctor_response.status_code == status.HTTP_404_NOT_FOUND:
            return Response({'message': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)
        elif current_user_role != 'Doctor':
            return Response({'message': 'Only doctors can create this.'}, status=status.HTTP_403_FORBIDDEN)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
