"""Filtrado de querysets por organización del usuario autenticado."""


def scoped_queryset(queryset, user, org_field='organization'):
    if user.is_superuser:
        return queryset
    org_id = getattr(user, 'organization_id', None)
    if not org_id:
        return queryset.none()
    return queryset.filter(**{f'{org_field}_id': org_id})


def organizations_for_user(user):
    from .models import Organization

    if user.is_superuser:
        return Organization.objects.all()
    org_id = getattr(user, 'organization_id', None)
    if not org_id:
        return Organization.objects.none()
    return Organization.objects.filter(pk=org_id)


def same_organization(user, other):
    if user.is_superuser:
        return True
    user_org_id = getattr(user, 'organization_id', None)
    other_org_id = getattr(other, 'organization_id', None)
    if not user_org_id or not other_org_id:
        return False
    return user_org_id == other_org_id
