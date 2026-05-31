from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer

User = get_user_model()


class ListCreateUser(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class FindUserByEmail(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        email = self.kwargs['email']
        return User.objects.filter(email__iexact=email)


class FindUserByName(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        name = self.kwargs['name']
        return User.objects.filter(full_name__icontains=name)


class UserDetailUpdate(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class LoginUserJWT(APIView):

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
            },
            status=status.HTTP_200_OK,
        )
