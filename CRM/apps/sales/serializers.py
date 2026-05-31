from rest_framework import serializers

from .models import CallLog, Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'agent',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')


class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLog
        fields = '__all__'
