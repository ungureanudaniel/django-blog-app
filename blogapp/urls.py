from django.urls import path
from django.conf.urls import url
from . import views
from .views import PostListView, PostDetailView, CategoryView, search, AboutView, ContactView

urlpatterns = [
    path('', PostListView, name='home'),
    path('results/', search, name='search'),
    path('post_detail/<str:slug>', PostDetailView, name='post_detail'),
    path('category_detail/<slug>/',CategoryView, name='category_detail'),
    path('about/', AboutView, name='about'),
    path('contact/', ContactView, name='contact'),
]
