from django.contrib import admin
from .models import Post

# Needs some TLC that I'm simply not able to give at the moment. "Functions."

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'poster', 'publish', 'status', 'id']
    list_filter = ['poster', 'publish', 'status']
    search_fields = ['title', 'id']
    date_hierarchy = 'publish'
    ordering = ['-status', 'id', 'poster', 'title']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'body']
    ordering = ['active', 'post', 'created']

admin.site.register(Post, PostAdmin)