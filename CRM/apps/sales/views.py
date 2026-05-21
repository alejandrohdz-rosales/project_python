from rest_framework.generics import ListAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateAPIView

# Serializers
from .serializers import *

# Create your views here.
class ListCustomers(ListCreateAPIView):
    serializer_class = CustomerSerializer
    queryset = CustomerModel.objects.all()

class CustomerDetailUpdate(RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer
    queryset = CustomerModel.objects.all()

class FindCustomerByName(ListAPIView):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        name = self.kwargs['name'].capitalize()
        queryset = CustomerModel.objects.get_customer_by_name(name)
        return queryset

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

class CallLogListCreateView(ListCreateAPIView):
    serializer_class = CallSerializer
    queryset = CallLogModel.objects.all()
