from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.organizations.tenancy import scoped_queryset

from .permissions import IsAdmin, IsAdminOrReadOnly, IsAdminOrSelf, IsAdminOrManager
from .serializers import UserSerializer

User = get_user_model()


class OrganizationScopedMixin:

    def get_queryset(self):
        return scoped_queryset(User.objects.all(), self.request.user)


class ListCreateUser(OrganizationScopedMixin, ListCreateAPIView):
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsAdminOrManager()]

class FindUserByEmail(OrganizationScopedMixin, ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        email = self.kwargs['email']
        return super().get_queryset().filter(email__iexact=email)


class FindUserByName(OrganizationScopedMixin, ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        name = self.kwargs['name']
        return super().get_queryset().filter(full_name__icontains=name)


class UserDetailUpdate(OrganizationScopedMixin, RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSelf]


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
