from django.urls import path

from django.conf import settings
from . import views
from django.conf.urls.static import static
from .views import PostListView, PostDetailView, CategoryView, search, AboutView, ContactView, SubscribeView

urlpatterns = [
    path('', PostListView, name='home'),
    path('results/', search, name='search'),
    path('post_detail/<str:slug>', PostDetailView, name='post_detail'),
    path('category_detail/<slug>/',CategoryView, name='category_detail'),
    path('about/', AboutView, name='about'),
    path('contact/', ContactView, name='contact'),
    path('signin/', SubscribeView, name='signin'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
