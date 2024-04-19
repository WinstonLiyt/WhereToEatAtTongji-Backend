from django.db import models
from django.contrib.postgres.fields import ArrayField
from usermodels import User

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=50, null=True, blank=True)
    num_thumbups = models.IntegerField(default=0)
    num_stars = models.IntegerField(default=0)
    images = ArrayField(models.CharField(max_length=2000), blank=True)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    is_post_comment = models.BooleanField()        # 如果是True，说明是该帖子的评论；如果是False，则说明是该帖子下评论的评论
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    ip = models.CharField(max_length=50)
    content = models.TextField()
    num_thumbups = models.IntegerField(default=0)
