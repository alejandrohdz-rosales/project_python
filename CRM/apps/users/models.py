from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.organizations.models import AuditModel, Organization

from .managers import UserManager


class User(AbstractBaseUser, AuditModel, PermissionsMixin):

    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'

    class Role(models.TextChoices):
        SALES_PERSON = 'SP', 'Sales Person'
        MANAGER = 'MG', 'Manager'
        ADMIN = 'AD', 'Admin'

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name='users',
    )
    email = models.EmailField('Email', unique=True)
    full_name = models.CharField('Full name', max_length=100)
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        default=Gender.OTHER,
    )
    role = models.CharField(
        max_length=2,
        choices=Role.choices,
        default=Role.SALES_PERSON,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return self.email
