from rest_framework.permissions import BasePermission

from apps.organizations.tenancy import same_organization, scoped_queryset
from apps.users.models import User

from .models import CallLog, Customer


def can_access_all_sales_data(user):
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or user.role in (User.Role.ADMIN, User.Role.MANAGER)
        )
    )


def customers_for_user(user):
    queryset = scoped_queryset(Customer.objects.all(), user)
    if can_access_all_sales_data(user):
        return queryset
    return queryset.filter(agent=user)


def calls_for_user(user):
    queryset = scoped_queryset(
        CallLog.objects.select_related('customer'),
        user,
        org_field='customer__organization',
    )
    if can_access_all_sales_data(user):
        return queryset
    return queryset.filter(customer__agent=user)


class IsCustomerOwnerOrManager(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not same_organization(user, obj):
            return False
        if can_access_all_sales_data(user):
            return True
        return obj.agent_id == user.pk
