from django.db import models


class AuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Organization(AuditModel):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'organization'
        verbose_name_plural = 'organizations'
        ordering = ['name']

    def __str__(self):
        return self.name
