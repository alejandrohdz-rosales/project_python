from rest_framework import serializers

from apps.organizations.models import Organization
from apps.organizations.serializers import OrganizationSerializer

from .models import User


class UserReadSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'organization',
            'full_name',
            'email',
            'gender',
            'role',
        )


class UserWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'},
    )
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        source='organization',
        required=False,
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            'id',
            'organization_id',
            'full_name',
            'email',
            'gender',
            'role',
            'password',
        )

    def validate(self, attrs):
        if self.instance is None and not attrs.get('password'):
            raise serializers.ValidationError(
                {'password': 'This field is required.'}
            )

        request = self.context.get('request')
        organization = attrs.get('organization')

        if self.instance:
            organization = organization or self.instance.organization
        elif request and not request.user.is_superuser:
            attrs['organization'] = request.user.organization
        elif request and request.user.is_superuser and not organization:
            raise serializers.ValidationError(
                {'organization_id': 'This field is required.'}
            )

        if self.instance and request and request.user.role != User.Role.ADMIN and not request.user.is_superuser:
            if 'role' in attrs and attrs['role'] != self.instance.role:
                raise serializers.ValidationError(
                    {'role': 'Only admins can change roles.'}
                )
            if 'email' in attrs and attrs['email'] != self.instance.email:
                raise serializers.ValidationError(
                    {'email': 'Only admins can change email.'}
                )
            if 'organization' in attrs and attrs['organization'] != self.instance.organization:
                raise serializers.ValidationError(
                    {'organization_id': 'Only admins can change organization.'}
                )

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        if request and not request.user.is_superuser:
            validated_data['organization'] = request.user.organization

        password = validated_data.pop('password')
        return User.objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance