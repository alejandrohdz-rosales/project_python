from django.shortcuts import render
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
User = get_user_model()
# Create your views here.
class ListCreateUser(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class FindUserByUsername(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        queryset = User.objects.filter(username=username)
        return queryset

class FindUserByName(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        name = self.kwargs['name'].capitalize()
        queryset = User.objects.filter(first_name=name)
        return queryset

class UserDetailUpdate(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()