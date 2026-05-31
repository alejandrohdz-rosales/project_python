from rest_framework.generics import ListAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from django.contrib.auth import get_user_model
# Serializers
from .serializers import *
User = get_user_model()
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

class CallLogListCreateView(ListCreateAPIView):
    serializer_class = CallSerializer
    queryset = CallLogModel.objects.all()
