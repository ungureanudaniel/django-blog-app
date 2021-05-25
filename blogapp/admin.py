from django.contrib import admin
from .models import Post, About, Comment, Category

class CategoryAdmin(admin.ModelAdmin):
     list_display = ('name', 'image')

class PostAdmin(admin.ModelAdmin):
     list_display = ('id', 'title', 'status', 'category', 'created_date',)
     list_filter = ('status',)
     search_fields = ('title', 'text',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(About)
admin.site.register(Comment)
