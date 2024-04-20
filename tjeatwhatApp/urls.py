from django.urls import path
from . import views

urlpatterns = [
    path('posts/search/', views.search_posts, name='search_posts'),
    path('posts/details/<int:id>/', views.get_one_post, name='get_one_post'),
    path('posts/getcomments/', views.get_children_comments, name='get_children_comments'),
]
