from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.conf import settings

# Create your models here.
#blog post categories
class Category(models.Model):
    name = models.CharField(max_length=20)
    image = models.FileField(upload_to='category_image', blank=True)

    def __str__(self):
        return self.name


#blog posts structure
class Post(models.Model):
    STATUS_CHOICES = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='blog_image', blank=True)
    text = models.TextField()
    category = models.CharField(max_length=20, default='Recipes')
    comment_count = models.IntegerField(default=0)
    featured = models.BooleanField()
    #seo_title = models.CharField(max_length=60, blank=True, null=True)
    #seo_text = models.CharField(max_length=165, blank=True, null=True)
    #slug = models.SlugField(max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    #updated_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='Draft', choices=STATUS_CHOICES)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.title

#blog post about section
class About(models.Model):
    title = models.CharField(max_length=250)
    text = models.CharField(max_length=600)

    def __str__(self):
        return self.title
