from django.db import models

class CustomerManager(models.Manager):
    def get_customer_by_name(self, name):
        return self.filter(
            first_name = name
        )

class UserManager(models.Manager):
    def get_agent_by_usermane(self, username):
        return self.filter(
            username = username
        )