from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Doctor, Patient, Hospital


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help texts and disable browser suggestions/autocomplete
        for name, field in self.fields.items():
            field.help_text = ''
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs.update({
                'class': (existing + ' form-control').strip(),
                'autocomplete': 'off',
                'autocapitalize': 'none',
                'autocorrect': 'off',
                'spellcheck': 'false',
            })


class DoctorSignUpForm(CustomUserCreationForm):
    # Minimal, professional fields only
    specialty = forms.CharField(max_length=100)
    license_number = forms.CharField(max_length=50)

    def save(self, commit=True):
        # Create a Doctor subtype instance
        doctor = Doctor()
        # Copy base user fields via the form
        base_user = super().save(commit=False)
        doctor.username = base_user.username
        doctor.email = base_user.email
        doctor.first_name = base_user.first_name
        doctor.last_name = base_user.last_name
        # Mark role for compatibility
        doctor.role = User.Roles.DOCTOR
        # Set password
        doctor.set_password(self.cleaned_data.get('password1'))
        # Doctor-specific fields
        doctor.specialty = self.cleaned_data['specialty']
        doctor.license_number = self.cleaned_data['license_number']
        if commit:
            doctor.save()
        return doctor


class PatientSignUpForm(CustomUserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Male','Male'),('Female','Female'),('Other','Other')])
    blood_group = forms.CharField(max_length=3, required=False)
    medical_history = forms.CharField(widget=forms.Textarea, required=False)
    emergency_contact_name = forms.CharField(max_length=100, required=False)
    emergency_contact_phone = forms.CharField(max_length=20, required=False)

    def save(self, commit=True):
        patient = Patient()
        base_user = super().save(commit=False)
        patient.username = base_user.username
        patient.email = base_user.email
        patient.first_name = base_user.first_name
        patient.last_name = base_user.last_name
        patient.role = User.Roles.PATIENT
        patient.set_password(self.cleaned_data.get('password1'))
        patient.date_of_birth = self.cleaned_data['date_of_birth']
        patient.gender = self.cleaned_data['gender']
        patient.blood_group = self.cleaned_data.get('blood_group', '')
        patient.medical_history = self.cleaned_data.get('medical_history', '')
        patient.emergency_contact_name = self.cleaned_data.get('emergency_contact_name', '')
        patient.emergency_contact_phone = self.cleaned_data.get('emergency_contact_phone', '')
        if commit:
            patient.save()
        return patient


class HospitalSignUpForm(CustomUserCreationForm):
    # Minimal, professional fields only
    hospital_name = forms.CharField(max_length=150)
    registration_number = forms.CharField(max_length=50)
    address = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove username, first and last name fields from the form
        for field in ('username', 'first_name', 'last_name'):
            self.fields.pop(field, None)
        # Ensure email is required for contact
        if 'email' in self.fields:
            self.fields['email'].required = True

    def save(self, commit=True):
        hospital = Hospital()
        # Derive username from registration_number, keep names empty
        hospital.username = self.cleaned_data['registration_number']
        base_user = super().save(commit=False)
        hospital.email = base_user.email
        hospital.first_name = ''
        hospital.last_name = ''
        hospital.role = User.Roles.HOSPITAL
        hospital.set_password(self.cleaned_data.get('password1'))
        hospital.hospital_name = self.cleaned_data['hospital_name']
        hospital.registration_number = self.cleaned_data['registration_number']
        hospital.address = self.cleaned_data['address']
        if commit:
            hospital.save()
        return hospital