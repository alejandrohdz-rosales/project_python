from rest_framework import serializers
from .models import CustomerModel, CallLogModel
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone',
            'agent_id',
        )

class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLogModel
        fields = '__all__'