from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("auth_app.urls")),
    path('',include("book_app.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('auth_app.urls')),
]
