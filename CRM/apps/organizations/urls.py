from django.urls import path

from . import views

urlpatterns = [
    path('organizations/', views.OrganizationListCreate.as_view(), name='organization-list'),
    path(
        'organizations/<int:pk>/',
        views.OrganizationDetail.as_view(),
        name='organization-detail',
    ),
]
