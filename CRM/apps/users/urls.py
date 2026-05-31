from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListCreateUser.as_view(), name='user-list'),
    path('users/username/<str:username>', views.FindUserByUsername.as_view(), name='user-find-username'),
    path('users/name/<name>/', views.FindUserByName.as_view(), name='user-find-name'),
    path('users/<int:pk>/', views.UserDetailUpdate.as_view(), name='user-update'),
]