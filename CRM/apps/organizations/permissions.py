from rest_framework.permissions import BasePermission, SAFE_METHODS

from apps.users.models import User


class IsSuperuser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsOrganizationMember(BasePermission):
    """Usuario autenticado con organización asignada (o superuser)."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return bool(request.user.organization_id)


class CanManageOrganization(BasePermission):
    """Superuser: cualquier org. Admin de la org: solo la suya (lectura/escritura)."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            return True
        if user.organization_id != obj.pk:
            return False
        if request.method in SAFE_METHODS:
            return True
        return user.role == User.Role.ADMIN
