from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListCreateUser.as_view(), name='user-list'),
    path('me/', views.MeUserView.as_view(), name='user-me'),
    path('login/', views.LoginUserJWT.as_view(), name='user-login'),
    path('email/<str:email>/', views.FindUserByEmail.as_view(), name='user-find-email'),
    path('name/<name>/', views.FindUserByName.as_view(), name='user-find-name'),
    path('<int:pk>/', views.UserDetailUpdate.as_view(), name='user-update'),
]