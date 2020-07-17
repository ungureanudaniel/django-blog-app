
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogapp.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/', include('authentication.urls')),

]
