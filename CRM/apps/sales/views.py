from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView

from .models import CallLog, Customer
from .serializers import CallSerializer, CustomerSerializer

User = get_user_model()


class ListCustomers(ListCreateAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class CustomerDetailUpdate(RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class FindCustomerByName(ListAPIView):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        name = self.kwargs['name']
        return Customer.objects.get_customers_by_name(name)


class CallLogListCreateView(ListCreateAPIView):
    serializer_class = CallSerializer
    queryset = CallLog.objects.all()
