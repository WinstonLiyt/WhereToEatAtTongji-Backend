from django.urls import path
from . import views

urlpatterns = [
    path('posts/search/', views.search_posts, name='search_posts'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/delete/', views.delete_post, name='delete_post'),
    path('posts/comment/', views.comment_post, name='comment_post'),
    path('posts/details/', views.get_one_post, name='get_one_post'),
    path('posts/getcomments/', views.get_children_comments, name='get_children_comments'),
    path('posts/reply_comment/', views.reply_comment, name='reply_comment'),
    path('posts/change_post_reaction', views.change_post_reaction, name='change_reaction'),
    path('posts/delete_comment', views.delete_comment, name='delete_comment'),
    path('posts/change_comment_reaction', views.change_comment_reaction, name='delete_reply'),
   
]
