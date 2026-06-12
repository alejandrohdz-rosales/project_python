from rest_framework.permissions import BasePermission, SAFE_METHODS

from apps.organizations.tenancy import same_organization

from .models import User


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (
            user.is_superuser or user.role == User.Role.ADMIN
        )


class IsAdminOrSelf(BasePermission):

    # def has_permission(self, request, view):
    #     return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not same_organization(user, obj):
            return False
        return (
            user.is_superuser
            or user.role == User.Role.ADMIN
            or obj.pk == user.pk
        )


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return user.is_superuser or user.role == User.Role.ADMIN

class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (
            user.is_superuser
            or user.role in [User.Role.ADMIN, User.Role.MANAGER]
        )