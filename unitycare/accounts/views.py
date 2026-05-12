from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import json
import uuid

from .forms import DoctorSignUpForm, PatientSignUpForm, HospitalSignUpForm
from .models import User, Doctor, Patient, Hospital
from appointment.models import Appointment


def signup_doctor(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ensure session is set for new user
            user = authenticate(request, username=user.username, password=form.cleaned_data.get('password1')) or user
            login(request, user)
            return redirect('doctor_dashboard')
    else:
        form = DoctorSignUpForm()
    return render(request, 'accounts/signup_doctor.html', {'form': form})


def signup_patient(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(request, username=user.username, password=form.cleaned_data.get('password1')) or user
            login(request, user)
            return redirect('patient_dashboard')
    else:
        form = PatientSignUpForm()
    return render(request, 'accounts/signup_patient.html', {'form': form})


def signup_hospital(request):
    if request.method == 'POST':
        form = HospitalSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(request, username=user.username, password=form.cleaned_data.get('password1')) or user
            login(request, user)
            return redirect('hospital_dashboard')
    else:
        form = HospitalSignUpForm()
    return render(request, 'accounts/signup_hospital.html', {'form': form})


class RoleBasedLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.role == User.Roles.DOCTOR:
            return reverse('doctor_dashboard')
        if user.role == User.Roles.HOSPITAL:
            return reverse('hospital_dashboard')
        return reverse('patient_dashboard')


@login_required
def dashboard(request):
    if request.user.role == User.Roles.DOCTOR:
        return redirect('doctor_dashboard')
    if request.user.role == User.Roles.HOSPITAL:
        return redirect('hospital_dashboard')
    return redirect('patient_dashboard')


@login_required
def doctor_dashboard(request):
    appointments = Appointment.objects.filter(doctor=request.user).select_related('patient')[:8]
    stats = {
        'requested': Appointment.objects.filter(doctor=request.user, status=Appointment.Status.REQUESTED).count(),
        'confirmed': Appointment.objects.filter(doctor=request.user, status=Appointment.Status.CONFIRMED).count(),
        'completed': Appointment.objects.filter(doctor=request.user, status=Appointment.Status.COMPLETED).count(),
    }
    return render(request, 'dashboards/doctor.html', {'appointments': appointments, 'stats': stats})


@login_required
def patient_dashboard(request):
    patient_appointments = Appointment.objects.filter(patient=request.user)
    appointments = patient_appointments.select_related('doctor')[:8]
    doctors = Doctor.objects.all()[:6]
    stats = {
        'upcoming': patient_appointments.exclude(status__in=[Appointment.Status.CANCELLED, Appointment.Status.COMPLETED]).count(),
        'doctors': Doctor.objects.count(),
        'completed': patient_appointments.filter(status=Appointment.Status.COMPLETED).count(),
    }
    return render(request, 'dashboards/patient.html', {
        'appointments': appointments,
        'doctors': doctors,
        'stats': stats,
    })


@login_required
def hospital_dashboard(request):
    status_counts = Appointment.objects.values('status').annotate(total=Count('id')).order_by('status')
    stats = {
        'patients': Patient.objects.count(),
        'doctors': Doctor.objects.count(),
        'appointments': Appointment.objects.count(),
        'requests': Appointment.objects.filter(status=Appointment.Status.REQUESTED).count(),
    }
    return render(request, 'dashboards/hospital.html', {
        'stats': stats,
        'status_counts': status_counts,
        'recent_appointments': Appointment.objects.select_related('patient', 'doctor')[:10],
    })


@login_required
def appointments_view(request):
    return render(request, 'appointments.html')


@login_required
def teleconferencing_view(request):
    return render(request, 'teleconferencing.html')


def hospitals_list(request):
    # Public page: list all users with role HOSPITAL or Hospital subtype
    from .models import User, Hospital
    hospitals_qs = Hospital.objects.all().select_related(None)
    # include base users with role HOSPITAL who may not have Hospital subtype (if any)
    base_hospitals_qs = User.objects.filter(role=User.Roles.HOSPITAL).exclude(id__in=hospitals_qs.values_list('id', flat=True))

    # Normalize to a simple dict list for template
    def hospital_dict(u):
        full_name = (u.get_full_name() or u.username).strip()
        return {
            'id': u.id,
            'name': full_name,
            'username': u.username,
            'email': u.email,
            'address': getattr(u, 'address', ''),
        }

    hospitals = [hospital_dict(u) for u in list(hospitals_qs)] + [hospital_dict(u) for u in list(base_hospitals_qs)]
    # Sort by name
    hospitals.sort(key=lambda h: h['name'].lower())
    return render(request, 'accounts/hospitals_list.html', { 'hospitals': hospitals })


def doctors_list(request):
    # Public page: list all users with role DOCTOR or Doctor subtype
    from .models import User, Doctor
    doctors_qs = Doctor.objects.all().select_related(None)
    # include base users with role DOCTOR who may not have Doctor subtype (if any)
    base_doctors_qs = User.objects.filter(role=User.Roles.DOCTOR).exclude(id__in=doctors_qs.values_list('id', flat=True))

    # Normalize to a simple dict list for template
    def doctor_dict(u):
        full_name = (u.get_full_name() or u.username).strip()
        return {
            'id': u.id,
            'name': full_name,
            'username': u.username,
            'email': u.email,
            'specialty': getattr(u, 'specialty', ''),
        }

    doctors = [doctor_dict(u) for u in list(doctors_qs)] + [doctor_dict(u) for u in list(base_doctors_qs)]
    # Sort by name
    doctors.sort(key=lambda d: d['name'].lower())
    return render(request, 'accounts/doctors_list.html', { 'doctors': doctors })


def doctors_list_api(request):
    # JSON API for doctors list used by patient booking dropdown
    from django.http import JsonResponse
    from .models import User, Doctor
    doctors_qs = Doctor.objects.all().select_related(None)
    base_doctors_qs = User.objects.filter(role=User.Roles.DOCTOR).exclude(id__in=doctors_qs.values_list('id', flat=True))

    def doctor_dict(u):
        full_name = (u.get_full_name() or u.username).strip()
        return {
            'id': u.id,
            'name': full_name,
            'specialty': getattr(u, 'specialty', ''),
        }

    doctors = [doctor_dict(u) for u in list(doctors_qs)] + [doctor_dict(u) for u in list(base_doctors_qs)]
    doctors.sort(key=lambda d: d['name'].lower())
    return JsonResponse(doctors, safe=False)


@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.username = request.POST.get('username', '')
        
        # Handle role-specific fields
        if user.role == User.Roles.DOCTOR and hasattr(user, 'doctor'):
            user.doctor.specialty = request.POST.get('specialty', '')
            user.doctor.save()
        elif user.role == User.Roles.HOSPITAL and hasattr(user, 'hospital'):
            user.hospital.address = request.POST.get('address', '')
            user.hospital.save()
        
        user.save()
        return JsonResponse({'status': 'success'})
    
    return render(request, 'accounts/profile.html')


@login_required
def feedback_view(request):
    if request.method == 'POST':
        feedback_data = {
            'user_id': request.user.id,
            'user_email': request.user.email,
            'feedback_type': request.POST.get('feedback_type'),
            'subject': request.POST.get('subject'),
            'message': request.POST.get('message'),
            'rating': request.POST.get('rating', 0),
            'timestamp': str(timezone.now()) if 'timezone' in globals() else 'now'
        }
        
        # In a real application, you would save this to a database
        # For now, we'll just log it or save to a file
        print(f"Feedback received: {feedback_data}")
        
        return JsonResponse({'status': 'success', 'message': 'Feedback received'})
    
    return render(request, 'accounts/feedback.html')


@login_required
def report_problem_view(request):
    if request.method == 'POST':
        ticket_id = str(uuid.uuid4())[:8].upper()
        problem_data = {
            'ticket_id': ticket_id,
            'user_id': request.user.id,
            'user_email': request.user.email,
            'problem_type': request.POST.get('problem_type'),
            'severity': request.POST.get('severity'),
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'steps_to_reproduce': request.POST.get('steps_to_reproduce'),
            'browser_info': request.POST.get('browser_info'),
            'url': request.POST.get('url'),
            'timestamp': str(timezone.now()) if 'timezone' in globals() else 'now'
        }
        
        # In a real application, you would save this to a database
        # For now, we'll just log it or save to a file
        print(f"Problem reported: {problem_data}")
        
        return JsonResponse({'status': 'success', 'ticket_id': ticket_id})
    
    return render(request, 'accounts/report_problem.html')


def signup_redirect(request):
    """Generic signup view that redirects based on role parameter"""
    role = request.GET.get('role', 'patient').lower()
    
    if role == 'doctor':
        return redirect('signup_doctor')
    elif role == 'hospital':
        return redirect('signup_hospital')
    else:  # default to patient
        return redirect('signup_patient')
