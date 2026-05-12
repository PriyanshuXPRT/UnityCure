from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and getattr(request.user, 'role', '').upper() == 'PATIENT'


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and getattr(request.user, 'role', '').upper() == 'DOCTOR'