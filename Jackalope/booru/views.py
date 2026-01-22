from django.shortcuts import render
from django.http import Http404
from .models import Post

def post_list(request):
    posts = Post.viewable.all()
    return render(request, 'booru/post/list.html', {'posts': posts})

def post_view(request, id):
    try:
        post = Post.viewable.get(id=id)
    except Post.DoesNotExist:
        raise Http404('Post not found.')
    return render(request, 'booru/post/view.html', {'post': post})