from django.db.models import Q
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView

from .models import CallLog, Customer
from .permissions import (
    IsCustomerOwnerOrManager,
    calls_for_user,
    customers_for_user,
)
from .serializers import CallSerializer, CustomerSerializer


class CustomerQuerysetMixin:

    def get_queryset(self):
        return customers_for_user(self.request.user)


class ListCustomers(CustomerQuerysetMixin, ListCreateAPIView):
    serializer_class = CustomerSerializer


class CustomerDetailUpdate(CustomerQuerysetMixin, RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsCustomerOwnerOrManager]


class FindCustomerByName(CustomerQuerysetMixin, ListAPIView):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        name = self.kwargs['name']
        return super().get_queryset().filter(
            Q(first_name__icontains=name) | Q(last_name__icontains=name)
        )


class CallLogListCreateView(ListCreateAPIView):
    serializer_class = CallSerializer

    def get_queryset(self):
        return calls_for_user(self.request.user)
