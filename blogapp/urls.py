from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from .views import PostListView, PostDetailView, PostDeleteView, CategoryView, search, AboutView, ContactView, AddPostView, AddCategoryView, DraftListView, PostEditView, PostDeleteView


urlpatterns = [
    path('', PostListView, name='home'),
    path('draft_posts', DraftListView, name='draft_posts'),
    path('results/', search, name='search'),
    path('add_post/', AddPostView, name='add_post'),
    path('add_category/', AddCategoryView, name='add_category'),
    path('post_detail/<int:pk>', PostDetailView, name='post_detail'),
    path('post_detail/edit/<int:pk>', PostEditView, name='post_edit'),
    path('post_detail/delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('category/<str:cats>/', CategoryView, name='category'),
    path('about/', AboutView, name='about'),
    path('contact/', ContactView, name='contact'),
    #search url
    path('search/', search, name='search'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
