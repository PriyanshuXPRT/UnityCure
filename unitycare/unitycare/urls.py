
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import TemplateView
from accounts.views import doctors_list_api

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('test-navbar/', TemplateView.as_view(template_name='test_navbar.html'), name='test_navbar'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('telecon/', include('telecon.urls')),
    path('api/doctors/', doctors_list_api),
    path('api/', include('appointment.urls')),
    
    # Password management
    path('accounts/password-change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change.html',
        success_url='/accounts/password-change/done/'
    ), name='password_change'),
    path('accounts/password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name='password_change_done'),
]
