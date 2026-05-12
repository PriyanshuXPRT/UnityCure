from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'scheduled_for', 'status', 'created_at')
    list_filter = ('status', 'scheduled_for', 'created_at')
    search_fields = ('patient__username', 'doctor__username', 'reason')