from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListCreateUser.as_view(), name='user-list'),
    path('login/', views.LoginUserJWT.as_view(), name='user-login'),
    path('users/email/<str:email>/', views.FindUserByEmail.as_view(), name='user-find-email'),
    path('users/name/<name>/', views.FindUserByName.as_view(), name='user-find-name'),
    path('users/<int:pk>/', views.UserDetailUpdate.as_view(), name='user-update'),
]