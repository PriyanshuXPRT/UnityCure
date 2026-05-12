from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Doctor, Patient, Hospital


class AdminUserCreationForm(UserCreationForm):
    """Admin add-user form that includes the custom 'role' field."""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name", "role")


class AdminUserChangeForm(UserChangeForm):
    """Admin change-user form that includes the custom 'role' field."""
    class Meta(UserChangeForm.Meta):
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Use custom forms so 'role' appears in both add and change forms
    form = AdminUserChangeForm
    add_form = AdminUserCreationForm

    # Show 'role' in the change page
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )

    # Show 'role' in the add page
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role', {'fields': ('role',)}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = BaseUserAdmin.list_filter + ('role',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'specialty', 'license_number', 'years_of_experience')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'specialty', 'license_number')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_of_birth', 'gender', 'blood_group')
    search_fields = ('username', 'first_name', 'last_name', 'email')


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('hospital_name', 'email', 'registration_number', 'bed_capacity')
    search_fields = ('hospital_name', 'email', 'registration_number', 'address')
