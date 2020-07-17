from django.contrib import admin
from .models import Post, Category, About, Comment

class CategoryAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'category', 'created_date',)
    list_filter = ('status',)
    search_fields = ('title', 'text',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(About)
admin.site.register(Comment)
