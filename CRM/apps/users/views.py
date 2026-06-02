from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.organizations.tenancy import scoped_queryset

from .permissions import IsAdmin, IsAdminOrReadOnly, IsAdminOrSelf, IsAdminOrManager
from .serializers import UserReadSerializer, UserWriteSerializer

User = get_user_model()


class OrganizationScopedMixin:
    def get_queryset(self):
        return scoped_queryset(User.objects.all(), self.request.user)


class ReadWriteSerializerMixin:
    read_serializer_class = None
    write_serializer_class = None

    def get_serializer_class(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return self.read_serializer_class
        return self.write_serializer_class


class ListCreateUser(OrganizationScopedMixin, ReadWriteSerializerMixin, ListCreateAPIView):
    read_serializer_class = UserReadSerializer
    write_serializer_class = UserWriteSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsAdminOrManager()]


class FindUserByEmail(OrganizationScopedMixin, ListAPIView):
    serializer_class = UserReadSerializer
    permission_classes = [IsAdminOrManager]

    def get_queryset(self):
        email = self.kwargs['email']
        return super().get_queryset().filter(email__iexact=email)


class FindUserByName(OrganizationScopedMixin, ListAPIView):
    serializer_class = UserReadSerializer
    permission_classes = [IsAdminOrManager]

    def get_queryset(self):
        name = self.kwargs['name']
        return super().get_queryset().filter(full_name__icontains=name)


class UserDetailUpdate(OrganizationScopedMixin, ReadWriteSerializerMixin, RetrieveUpdateAPIView):
    read_serializer_class = UserReadSerializer
    write_serializer_class = UserWriteSerializer
    permission_classes = [IsAdminOrSelf]


class MeUserView(ReadWriteSerializerMixin, RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    read_serializer_class = UserReadSerializer
    write_serializer_class = UserWriteSerializer

    def get_object(self):
        return self.request.user