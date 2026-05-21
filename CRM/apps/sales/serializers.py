from rest_framework import serializers
from .models import CustomerModel, User, CallLogModel

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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )
class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLogModel
        fields = '__all__'