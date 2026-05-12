from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        DOCTOR = 'DOCTOR', 'Doctor'
        PATIENT = 'PATIENT', 'Patient'
        HOSPITAL = 'HOSPITAL', 'Hospital'

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.PATIENT)

    def __str__(self) -> str:
        return f"{self.username} ({self.get_role_display()})"


# Role-specific profiles are now deprecated and replaced by multi-table inheritance
# These models will be removed in a subsequent migration after data move.


# Multi-table inheritance subtypes (Option 3)
class Doctor(User):
    specialty = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    clinic_address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        return f"Doctor: {self.username}"


class Patient(User):
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=[('Male','Male'),('Female','Female'),('Other','Other')])
    blood_group = models.CharField(max_length=3, blank=True)
    medical_history = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    def __str__(self):
        return f"Patient: {self.username}"


class Hospital(User):
    hospital_name = models.CharField(max_length=150)
    registration_number = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=20, blank=True)
    bed_capacity = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Hospital'
        verbose_name_plural = 'Hospitals'

    def __str__(self):
        return f"Hospital: {self.hospital_name}"