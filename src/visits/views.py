from rest_framework import status
from rest_framework.mixins import UpdateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
import requests

from .models import Visit
from .serializers import VisitSerializer
from core.settings import HTTP_URL


class VisitView(GenericViewSet, UpdateModelMixin, ListModelMixin, RetrieveModelMixin):
    serializer_class = VisitSerializer
    permission_classes = [AllowAny]
    queryset = Visit.objects.all()

    def _list_visits(self, queryset):
        """Helper method for listing and paginating visits"""
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='patient/(?P<patient_id>\d+)')
    def get_patient_visits(self, request, patient_id=None):
        queryset = self.get_queryset().filter(patient_id=patient_id)
        return Response(self._list_visits(queryset))

    @action(methods=['GET'], detail=False, url_path='doctor/(?P<doctor_id>\d+)')
    def get_doctor_visits(self, request, doctor_id=None):
        queryset = self.get_queryset().filter(doctor_id=doctor_id)

        start_date = request.query_params.get('start_date')
        stop_date = request.query_params.get('stop_date')

        if start_date and stop_date:
            queryset = queryset.filter(date__range=(start_date, stop_date))

        return Response(self._list_visits(queryset))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        accounts_service_url = f'{HTTP_URL}/users/'

        patient_id = self.request.data.get('patient_id')
        patient_url = f'{accounts_service_url}{patient_id}/'

        patient_response = requests.get(patient_url)

        if patient_response.status_code == status.HTTP_404_NOT_FOUND:
            return Response({'message': 'Patient not found.'}, status=status.HTTP_404_NOT_FOUND)

        doctor_id = self.request.data.get('doctor_id')
        doctor_url = f'{accounts_service_url}{doctor_id}/'

        doctor_response = requests.get(doctor_url)

        if doctor_response.status_code == status.HTTP_404_NOT_FOUND:
            return Response({'message': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['DELETE'], detail=False, url_path='delete/(?P<visit_id>\d+)')
    def soft_delete_visit(self, request, visit_id=None):
        current_user_role = self.request.headers.get('role')

        if current_user_role != 'Doctor':
            return Response({'message': 'Only doctors can delete visit.'}, status=status.HTTP_403_FORBIDDEN)

        visit = Visit.everything.get(id=visit_id)
        if visit.is_deleted:
            return Response({'message': 'That visit was deleted.'}, status=status.HTTP_404_NOT_FOUND)

        visit.soft_deleted()

        return Response(status=status.HTTP_204_NO_CONTENT)
