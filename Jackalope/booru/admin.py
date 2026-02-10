from django.contrib import admin
from .models import Post
from .models import Tag

# Needs some TLC that I'm simply not able to give at the moment. "Functions."

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'poster', 'publish', 'status', 'id']
    list_filter = ['poster', 'publish', 'status']
    search_fields = ['title', 'id']
    date_hierarchy = 'publish'
    ordering = ['-status', 'id', 'poster', 'title']

class TagAdmin(admin.ModelAdmin):
    list_display = ['tagSlug', 'tagName', 'tagType', 'id']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'body']
    ordering = ['active', 'post', 'created']

admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)