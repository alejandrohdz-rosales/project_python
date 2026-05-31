from django.urls import path
from . import views
urlpatterns = [
    path('customers/', views.ListCustomers.as_view(), name='customer-list'),
    path('customers/<int:pk>/', views.CustomerDetailUpdate.as_view(), name='customer-detail'),
    path('customers/name/<name>/', views.FindCustomerByName.as_view(), name='customer-find-name'),
    path('calls/', views.CallLogListCreateView.as_view(), name='call-list'),
]