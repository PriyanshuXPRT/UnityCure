from django.conf import settings
from django.db import models
from django.utils import timezone


class Appointment(models.Model):
    class Status(models.TextChoices):
        REQUESTED = 'REQUESTED', 'Requested'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        COMPLETED = 'COMPLETED', 'Completed'

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments_as_patient'
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments_as_doctor'
    )
    scheduled_for = models.DateTimeField()
    reason = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.REQUESTED
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_for']
        constraints = [
            # Prevent patients booking themselves; also ensures a doctor and patient are not identical
            models.CheckConstraint(
                check=~models.Q(patient=models.F('doctor')),
                name='appointment_patient_not_doctor'
            )
        ]

    def __str__(self):
        return f"Appt: {self.patient} -> {self.doctor} at {self.scheduled_for:%Y-%m-%d %H:%M} ({self.status})"