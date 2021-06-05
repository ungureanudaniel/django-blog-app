from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
#----------------------VIEWS IMPORT------------------------------------------
from .views import PostListView, PostDetailView, PostDeleteView, search, AboutView, ContactView, AddPostView, \
    DraftListView, PostEditView, PostDeleteView, AddAboutView, EditAboutView, LoginView, LogoutView, \
    AddCategoryView, CategoryView
#------------------SITE MAP IMPORTS----------------------------------------
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap, AboutSitemap, StaticSitemap
from django.views.generic.base import TemplateView

sitemaps = {
    'post':PostSitemap,
    'about':AboutSitemap,
    'static':StaticSitemap
}

urlpatterns = [
    path('', PostListView, name='home'),
    path('draft_posts', DraftListView, name='draft_posts'),
    path('results/', search, name='search'),
    path('add_post/', AddPostView, name='add_post'),

    path('add_category/', AddCategoryView, name='add_category'),
    path('post_detail/<int:pk>', PostDetailView, name='post_detail'),
    path('post_edit/<int:pk>', PostEditView, name='post_edit'),
    path('post_detail/delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('category/<int:pk>/', CategoryView, name='category'),
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
    path('logout', LogoutView, name='logout'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path("robots.txt",TemplateView.as_view(template_name="blogapp/robots.txt", content_type="text/plain")),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
