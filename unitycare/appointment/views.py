from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .models import Appointment
from .serializers import (
    AppointmentCreateSerializer,
    AppointmentListSerializer,
    AppointmentStatusSerializer,
)

User = get_user_model()


class AppointmentViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Appointment.objects.all()
        # Patients see their own appointments; Doctors see theirs
        if getattr(user, 'role', '').upper() == 'PATIENT':
            return qs.filter(patient=user)
        if getattr(user, 'role', '').upper() == 'DOCTOR':
            return qs.filter(doctor=user)
        # other roles see nothing by default
        return qs.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return AppointmentCreateSerializer
        return AppointmentListSerializer

    def perform_create(self, serializer):
        # Ensure only patients can create appointments
        user = self.request.user
        if getattr(user, 'role', '').upper() != 'PATIENT':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only patients can create appointments')
        serializer.save()

    @action(detail=True, methods=['patch'])
    def status(self, request, pk=None):
        appointment = self.get_object()
        user = request.user
        if getattr(user, 'role', '').upper() != 'DOCTOR' or appointment.doctor_id != user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only the assigned doctor can update this appointment.')

        serializer = AppointmentStatusSerializer(appointment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(AppointmentListSerializer(appointment).data)
