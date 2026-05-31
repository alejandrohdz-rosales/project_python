from django.conf import settings
from django.db import models
from .managers import *
# Create your models here.

class CustomerModel(models.Model):
    objects = CustomerManager()

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    agent_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CallLogModel(models.Model):
    STATUS_CHOICES = [
        ('connected', 'Conectada'),
        ('no_answer', 'No contestó'),
        ('busy', 'Ocupado'),
        ('failed', 'Fallida'),
    ]

    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE, related_name='calls')
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='calls_made')
    call_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='connected')

    def __str__(self):
        return f"Call to {self.customer} - {self.call_date.strftime('%Y-%m-%d')}"