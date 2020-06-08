from django.contrib import admin
from .models import Post, Category

class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)

class PostAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('id', 'title', 'status', 'category', 'created_date', 'updated_date',)
    list_filter = ('status',)
    search_fields = ('title', 'text',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
