from django.urls import path
from . import views
urlpatterns = [
    path('customers/', views.ListCustomers.as_view(), name='customer-list'),
    path('customers/<int:pk>/', views.CustomerDetailUpdate.as_view(), name='customer-detail'),
    path('customers/name/<name>/', views.FindCustomerByName.as_view(), name='customer-find-name'),
    path('users/', views.ListCreateUser.as_view(), name='user-list'),
    path('users/username/<str:username>', views.FindUserByUsername.as_view(), name='user-find-username'),
    path('users/name/<name>/', views.FindUserByName.as_view(), name='user-find-name'),
    path('users/<int:pk>/', views.UserDetailUpdate.as_view(), name='user-update'),
    path('calls/', views.CallLogListCreateView.as_view(), name='call-list'),
]