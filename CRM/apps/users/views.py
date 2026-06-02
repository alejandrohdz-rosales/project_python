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
from .serializers import UserReadSerializer, UserWriteSerializer, MeUserWriteSerializer

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


class UserDetailUpdate(OrganizationScopedMixin, RetrieveUpdateAPIView):
    permission_classes = [IsAdminOrSelf]

    def get_serializer_class(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return UserReadSerializer

        obj = self.get_object()
        user = self.request.user

        if user.is_superuser or user.role == User.Role.ADMIN:
            return AdminUserWriteSerializer

        if obj.pk == user.pk:
            return MeUserWriteSerializer

        return UserWriteSerializer

class MeUserView(ReadWriteSerializerMixin, RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    read_serializer_class = UserReadSerializer
    write_serializer_class = MeUserWriteSerializer

    def get_object(self):
        obj = self.request.user
        self.check_object_permissions(self.request, obj)
        return obj
    

class LoginUserJWT(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'error': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(
            request,
            username=email,
            password=password,
        )

        if user is None or not user.is_active:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'organization_id': user.organization_id,
            },
            status=status.HTTP_200_OK,
        )