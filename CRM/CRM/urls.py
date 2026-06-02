from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.organizations.urls'), name='organizations-app'),
    path('', include('apps.users.urls'), name='user-app'),
    path('', include('apps.sales.urls'), name='sales-app'),
]
