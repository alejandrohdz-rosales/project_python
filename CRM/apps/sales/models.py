from django.conf import settings
from django.db import models

from apps.users.models import AuditModel

from .managers import CustomerManager


class Customer(AuditModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customers',
    )

    objects = CustomerManager()

    class Meta:
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class CallLog(models.Model):
    class Status(models.TextChoices):
        CONNECTED = 'connected', 'Conectada'
        NO_ANSWER = 'no_answer', 'No contestó'
        BUSY = 'busy', 'Ocupado'
        FAILED = 'failed', 'Fallida'

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='calls',
    )
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='calls_made',
    )
    call_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CONNECTED,
    )

    class Meta:
        verbose_name = 'call log'
        verbose_name_plural = 'call logs'
        ordering = ['-call_date']

    def __str__(self):
        return f'Call to {self.customer} - {self.call_date:%Y-%m-%d}'
