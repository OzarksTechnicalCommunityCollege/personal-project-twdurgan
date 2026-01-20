from django.contrib import admin
from .models import Post
from .models import Tag

# Register your models here.

admin.site.register(Post)
admin.site.register(Tag)

class PostAdmin(admin.ModelAdmin):
    list_display = ['poster', 'publish', 'status', 'id']

class TagAdmin(admin.ModelAdmin):
    list_display = ['tagName', 'tagSlug', 'id']