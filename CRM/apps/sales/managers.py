from django.db import models


class CustomerManager(models.Manager):
    def get_customers_by_name(self, name):
        return self.filter(
            models.Q(first_name__icontains=name) | models.Q(last_name__icontains=name)
        )
