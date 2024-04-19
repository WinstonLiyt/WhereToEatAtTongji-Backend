# 修一些报错
import django
from django.utils.encoding import smart_str
django.utils.encoding.smart_text = smart_str
from django.utils.translation import gettext
django.utils.translation.ugettext = gettext

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from rest_framework.decorators import authentication_classes, permission_classes
from models.communitymodels import Post, Comment
from models import User
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'user_name', 'images', 'label', 'user_avatar', 'num_upvotes', 'num_comments', 'num_stars', 'id']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['title', 'content', 'user_name', 'images', 'label', 'user_avatar', 'num_upvotes', 'num_comments', 'num_stars', 'id']




@csrf_exempt
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([])
def search_posts(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        content = request.POST.get('content', '')
        
        # 进行JWT验证
        try:
            user = User.objects.get(pk=request.user.id)
        except User.DoesNotExist:
            return JsonResponse({'message': 'Invalid token'}, status=400)
        
        # 搜索数据库中含有message的所有帖子
        posts = Post.objects.filter(content__icontains=content)  # 大小写不敏感
        posts = list(posts)

        # 将查询结果序列化为JSON格式
        print(posts)        
        # 构造返回结果
        response_data = {
            'message': 'Success',
            'posts': posts
        }
        
        return JsonResponse(response_data)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

@csrf_exempt
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([])
def get_one_post(request, id):
    if request.method == 'GET':
        # token = request.META.get('HTTP_AUTHORIZATION').split()[1]        
        # # 进行JWT验证
        # try:
        #     user = User.objects.get(pk=request.user.id)
        # except User.DoesNotExist:
        #     return JsonResponse({'message': 'Invalid token'}, status=400)
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return JsonResponse({'message': 'Post not found'}, status=404)
        
        print(post,type(post))
        parent_comments = Comment.objects.filter(is_post_comment=True, post_id=id)
        parent_comments = list(parent_comments)
        post['parent_comments'] = parent_comments
        children_comments = Comment.objects.filter(is_post_comment=False, post_id=id)
        children_comments = list(children_comments)
        for comment in parent_comments:
            pass
        # 构造返回结果
        response_data = {
            'message': 'Success',
            'post': post
        }
        
        return JsonResponse(response_data)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


def get_children_comments(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        # 处理JSON数据
        parent_id = json_data.get('parent_id', None)  # 获取JSON数据中的特定字段值
        post_id = json_data.get('post_id', None)  # 获取JSON数据中的特定字段值
        
        children_comments = Comment.objects.filter(is_post_comment=False, parent_id=parent_id, post_id=post_id)
        for comment in children_comments:
            comment.user_name = User.objects.get(pk=comment.user_id).username
            comment.user_avatar = User.objects.get(pk=comment.user_id).avatar

        # 构造返回结果
        response_data = {
            'message': 'Success',
            'children_comments': children_comments
        }
        
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)