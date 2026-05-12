from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import Doctor, Hospital, Patient
from appointment.models import Appointment


class Command(BaseCommand):
    help = "Create demo UnityCare users and one appointment request."

    def handle(self, *args, **options):
        doctor, _ = Doctor.objects.get_or_create(
            username="dr.sarah",
            defaults={
                "email": "dr.sarah@unitycare.test",
                "first_name": "Sarah",
                "last_name": "Johnson",
                "role": "DOCTOR",
                "specialty": "Cardiology",
                "license_number": "UC-DOC-1001",
                "years_of_experience": 12,
                "clinic_address": "UnityCare Heart Clinic",
            },
        )
        doctor.set_password("DemoPass123")
        doctor.role = "DOCTOR"
        doctor.save()

        patient, _ = Patient.objects.get_or_create(
            username="john.patient",
            defaults={
                "email": "john.patient@unitycare.test",
                "first_name": "John",
                "last_name": "Doe",
                "role": "PATIENT",
                "date_of_birth": "1990-01-15",
                "gender": "Male",
                "blood_group": "O+",
            },
        )
        patient.set_password("DemoPass123")
        patient.role = "PATIENT"
        patient.save()

        hospital, _ = Hospital.objects.get_or_create(
            username="unity-admin",
            defaults={
                "email": "admin@unitycare.test",
                "role": "HOSPITAL",
                "hospital_name": "UnityCare Admin",
                "registration_number": "UC-HOSP-1001",
                "address": "123 Healthcare Ave",
                "bed_capacity": 120,
            },
        )
        hospital.set_password("DemoPass123")
        hospital.role = "HOSPITAL"
        hospital.save()

        Appointment.objects.get_or_create(
            patient=patient,
            doctor=doctor,
            status=Appointment.Status.REQUESTED,
            defaults={
                "scheduled_for": timezone.now() + timedelta(days=1, hours=2),
                "reason": "Demo consultation request",
            },
        )

        self.stdout.write(self.style.SUCCESS("Demo users ready: john.patient, dr.sarah, unity-admin / DemoPass123"))
