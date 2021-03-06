from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import PostListView, PostDetailView, PostDeleteView, search, AboutView, ContactView, AddPostView, \
    DraftListView, PostEditView, PostDeleteView, AddAboutView, EditAboutView, LoginView, LogoutView, \
    AddCategoryView, CategoryView


urlpatterns = [
    path('', PostListView, name='home'),
    path('draft_posts', DraftListView, name='draft_posts'),
    path('results/', search, name='search'),
    path('add_post/', AddPostView, name='add_post'),

    path('add_category/', AddCategoryView, name='add_category'),
    path('post_detail/<int:pk>', PostDetailView, name='post_detail'),
    path('post_edit/<int:pk>', PostEditView, name='post_edit'),
    path('post_detail/delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('category/<str:cats>/', CategoryView, name='category'),
    #ABOUT ME URLS
    path('add_about/', AddAboutView, name='add_about'),
    path('about', AboutView, name='about'),
    path('edit_about/<int:pk>', EditAboutView, name='edit_about'),
    #CONTACT ME URLS
    path('contact/', ContactView, name='contact'),
    #search url
    path('search/', search, name='search'),
    #LOGIN
    path('login/', LoginView, name='login'),
    path('logout', LogoutView, name='logout')

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
