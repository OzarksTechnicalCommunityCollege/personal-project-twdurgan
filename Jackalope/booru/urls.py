from django.urls import path
from . import views

app_name = 'booru'

# I'm not (at the moment) going to be making easily-indexed URLs for posts; a large portion of the art community I intend this project to serve
    # prefers not to have their works indexable by search engines. SEO for individual posts would lend a discoverability to works people would likely prefer to only
    # share in-community. Also, posts are being designed with the intention of only requiring the image itself and maybe a few tags, so constructing a URL from those things
    # would likely be a messy process and lead to URLs that change frequently. Site and post navigation should be done on-site, via hyperlinks and a robust tag-searching feature.
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:id>/', views.post_view, name='post_view'),
]