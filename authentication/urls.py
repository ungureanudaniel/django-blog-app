from django.urls import path, include
from .views import SubscribeView, UnsubscribeView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('subscribe/', SubscribeView, name='subscribe'),
    path('unsubscribe/', UnsubscribeView, name='unsubscribe'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('oauth/', include('social_django.urls', namespace='social')),
]
