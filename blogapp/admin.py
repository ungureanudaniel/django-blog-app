from django.contrib import admin
from .models import Post, About, Comment, Category, Subscriber

class CategoryAdmin(admin.ModelAdmin):
     list_display = ('name', 'image', 'slug')
     prepopulated_fields = {'slug': ('name',), }
#
class SubscriberAdmin(admin.ModelAdmin):
     list_display = ('name', 'email', 'conf_num', 'voucher_prize', 'confirmed', 'timestamp')


class PostAdmin(admin.ModelAdmin):
     list_display = ('id', 'title', 'status', 'slug', 'category', 'created_date',)
     list_filter = ('status',)
     search_fields = ('title', 'text',)
     prepopulated_fields = {'slug': ('title',), }

class AboutAdmin(admin.ModelAdmin):
     list_display = ('title', 'text', 'image2', 'image3')



admin.site.register(Category, CategoryAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(Comment)
