from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.conf import settings
from ckeditor.fields import RichTextField

# Create your models here.
#blog post categories
class Category(models.Model):
    name = models.CharField(max_length=20)
    image = models.FileField(upload_to='category_image', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')


#blog posts structure
class Post(models.Model):
    STATUS_CHOICES = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='blog_image', blank=True)
    text = RichTextField(blank=True, null=True)
    #text = models.TextField()
    category = models.CharField(max_length=20, default='recipes')
    comment_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    featured = models.BooleanField()
    #seo_title = models.CharField(max_length=60, blank=True, null=True)
    #seo_text = models.CharField(max_length=165, blank=True, null=True)
    #slug = models.SlugField(max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    #updated_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='Draft', choices=STATUS_CHOICES)
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
        #return reverse('home')

    def get_edit_url(self):
        return reverse('post_edit', kwargs={'pk': self.pk})
        #return reverse('home')

    def get_delete_url(self):
        return reverse('post_delete', kwargs={'pk': self.pk})
        #return reverse('home')

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

#blog post comment section
class Comment(models.Model):
    user = models.ForeignKey(User, default="1", on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


#blog post about section
class About(models.Model):
    title = models.CharField(max_length=250)
    text = models.CharField(max_length=600)

    def __str__(self):
        return self.title


