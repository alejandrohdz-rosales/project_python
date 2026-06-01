from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The user must have an email.')
        if not extra_fields.get('full_name'):
            raise ValueError('The user must have a full name.')
        if not extra_fields.get('organization'):
            raise ValueError('The user must belong to an organization.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', self.model.Role.SALES_PERSON)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', self.model.Role.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if password is None:
            raise ValueError('Superuser must have a password.')

        if not extra_fields.get('organization'):
            from apps.organizations.models import Organization

            org, _ = Organization.objects.get_or_create(
                slug='platform',
                defaults={'name': 'Platform'},
            )
            extra_fields['organization'] = org

        return self._create_user(email, password, **extra_fields)
