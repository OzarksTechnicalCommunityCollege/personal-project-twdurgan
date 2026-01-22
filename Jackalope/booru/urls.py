from django.urls import path
from . import views

app_name = 'booru'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:id>/', views.post_view, name='post_view'),
]