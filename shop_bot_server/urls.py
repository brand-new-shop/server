from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('accounts.urls')),
    path('api/', include('support.urls')),
    path('api/', include('products.urls')),
    path('api/', include('info.urls')),
]
