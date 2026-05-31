from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.sales.urls'), name='prestamo-app'),
    path('', include('apps.users.urls'), name='user-app'),
]
