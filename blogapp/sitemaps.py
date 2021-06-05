from django.contrib.sitemaps import Sitemap
from .models import Post, About
from django.urls import reverse

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.created_date


class AboutSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return About.objects.all()

class StaticSitemap(Sitemap):
    changefreq = 'monthly'

    def items(self):
        return ['home', 'about', 'contact']

    def location(self, item):
        return reverse(item)
