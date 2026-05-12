from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Appointment

User = get_user_model()


class AppointmentCreateSerializer(serializers.ModelSerializer):
    # Only allow patient to set doctor and schedule; patient id comes from request user
    doctor = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='DOCTOR'))
    scheduled_for = serializers.DateTimeField()

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'scheduled_for', 'reason']

    def validate_scheduled_for(self, value):
        from django.utils import timezone
        if value <= timezone.now():
            raise serializers.ValidationError('scheduled_for must be in the future')
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        # Force the patient to be current user
        return Appointment.objects.create(patient=user, **validated_data)


class AppointmentListSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    telecon_room = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'scheduled_for', 'reason', 'status', 'telecon_room', 'created_at', 'updated_at'
        ]
        read_only_fields = fields

    def get_telecon_room(self, obj):
        return f"appointment-{obj.id}"


class AppointmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['status']

    def validate_status(self, value):
        allowed = {
            Appointment.Status.CONFIRMED,
            Appointment.Status.CANCELLED,
            Appointment.Status.COMPLETED,
        }
        if value not in allowed:
            raise serializers.ValidationError('Doctors can confirm, cancel, or complete appointments.')
        return value
