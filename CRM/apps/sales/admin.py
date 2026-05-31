from django.contrib import admin

from .models import CallLog, Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'agent', 'created_at')
    list_filter = ('agent',)
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('-created_at',)


@admin.register(CallLog)
class CallLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'agent', 'status', 'call_date')
    list_filter = ('status', 'call_date')
    search_fields = ('customer__first_name', 'customer__last_name', 'notes')
    ordering = ('-call_date',)
