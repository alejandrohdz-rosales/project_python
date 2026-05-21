from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import CustomerModel, CallLogModel
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name'
    )

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
    )
admin.site.register(CustomerModel, CustomerAdmin)
admin.site.register(CallLogModel)