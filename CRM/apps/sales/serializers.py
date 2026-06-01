from rest_framework import serializers

from apps.users.models import User

from .models import CallLog, Customer
from .permissions import can_access_all_sales_data, customers_for_user


class CustomerSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Customer
        fields = (
            'id',
            'organization',
            'first_name',
            'last_name',
            'email',
            'phone',
            'agent',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at', 'organization')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.role == User.Role.SALES_PERSON:
            self.fields['agent'].read_only = True

    def validate_email(self, value):
        request = self.context.get('request')
        if not request:
            return value

        organization = request.user.organization
        qs = Customer.objects.filter(
            organization=organization,
            email__iexact=value,
        )
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                'A customer with this email already exists in your organization.'
            )
        return value

    def validate_agent(self, value):
        request = self.context.get('request')
        if not request:
            return value
        if can_access_all_sales_data(request.user):
            if value and not request.user.is_superuser:
                if value.organization_id != request.user.organization_id:
                    raise serializers.ValidationError(
                        'Agent must belong to your organization.'
                    )
            return value
        if value and value != request.user:
            raise serializers.ValidationError(
                'You can only assign yourself as agent.'
            )
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request:
            validated_data['organization'] = request.user.organization
            if request.user.role == User.Role.SALES_PERSON:
                validated_data['agent'] = request.user
        return super().create(validated_data)


class CallSerializer(serializers.ModelSerializer):

    class Meta:
        model = CallLog
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.role == User.Role.SALES_PERSON:
            self.fields['agent'].read_only = True
        if request and 'customer' in self.fields:
            self.fields['customer'].queryset = customers_for_user(request.user)

    def validate(self, attrs):
        request = self.context.get('request')
        if not request:
            return attrs

        user = request.user
        customer = attrs.get('customer') or getattr(self.instance, 'customer', None)

        if customer and not user.is_superuser:
            if customer.organization_id != user.organization_id:
                raise serializers.ValidationError(
                    {'customer': 'You do not have access to this customer.'}
                )

        if user.role == User.Role.SALES_PERSON:
            if customer is None or customer.agent_id != user.pk:
                raise serializers.ValidationError(
                    {'customer': 'You do not have access to this customer.'}
                )
            attrs['agent'] = user

        agent = attrs.get('agent')
        if agent and not user.is_superuser and agent.organization_id != user.organization_id:
            raise serializers.ValidationError(
                {'agent': 'Agent must belong to your organization.'}
            )

        return attrs
