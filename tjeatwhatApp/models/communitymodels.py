from django.db import models
from .usermodels import Users

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=50, null=True, blank=True)
    num_upvotes = models.IntegerField(default=0)
    num_stars = models.IntegerField(default=0)
    ip = models.CharField(max_length=50, null=True, blank=True)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    is_post_comment = models.BooleanField(default=True)          # 如果是True，说明是该帖子的评论；如果是False，则说明是该帖子下评论的评论
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    num_upvotes = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)


class PostImages(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=2000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Upvote(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Star(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class UpvoteComment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)