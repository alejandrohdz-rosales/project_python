from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('organizations/', include('apps.organizations.urls')),
    path('users/', include('apps.users.urls')),
    path('sales/', include('apps.sales.urls')),
]