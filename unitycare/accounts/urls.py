from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    RoleBasedLoginView,
    signup_doctor, signup_patient, signup_hospital, signup_redirect,
    dashboard, doctor_dashboard, patient_dashboard, hospital_dashboard,
    doctors_list, hospitals_list, appointments_view, teleconferencing_view,
    profile_view, feedback_view, report_problem_view,
)

urlpatterns = [
    path('login/', RoleBasedLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('signup/', signup_redirect, name='signup'),
    path('signup/doctor/', signup_doctor, name='signup_doctor'),
    path('signup/patient/', signup_patient, name='signup_patient'),
    path('signup/hospital/', signup_hospital, name='signup_hospital'),

    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/doctor/', doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/patient/', patient_dashboard, name='patient_dashboard'),
    path('dashboard/hospital/', hospital_dashboard, name='hospital_dashboard'),

    # Public directories
    path('doctors/', doctors_list, name='doctors_list'),
    path('hospitals/', hospitals_list, name='hospitals_list'),
    
    # Services
    path('appointments/', appointments_view, name='appointments'),
    path('teleconferencing/', teleconferencing_view, name='teleconferencing'),
    
    # Account management
    path('profile/', profile_view, name='profile'),
    path('feedback/', feedback_view, name='feedback'),
    path('report-problem/', report_problem_view, name='report_problem'),
]