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
from ..models.communitymodels import Post, Comment
from ..models.usermodels import Users
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'  # 或者指定您希望序列化的字段

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'  # 或者指定您希望序列化的字段

@csrf_exempt
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([])
def search_posts(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        # token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        content = json_data.get('content', None) 
        
        # 进行JWT验证
        # try:
        #     user = User.objects.get(pk=request.user.id)
        # except User.DoesNotExist:
        #     return JsonResponse({'message': 'Invalid token'}, status=400)
        
        # 搜索数据库中含有message的所有帖子
        posts = Post.objects.filter(content__icontains=content)  # 大小写不敏感
        if posts.exists():
            posts = list(posts)
            serializer = PostSerializer(posts, many=True)
            serialized_posts = serializer.data
            for post in serialized_posts:
                post['user_name'] = Users.objects.get(pk=post['user']).username
                post['user_avatar'] = Users.objects.get(pk=post['user']).avatar
                post['num_comments'] = Comment.objects.filter(post_id=post['id']).count()
        else:
            posts = []
        # 将查询结果序列化为JSON格式
        # 构造返回结果
        response_data = {
            'message': 'Success',
            'posts': serialized_posts
        }
        print('response_data_posts:', response_data)
        return JsonResponse(response_data, status=200)
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
        post = PostSerializer(post).data
        parent_comments = Comment.objects.filter(is_post_comment=True, post_id=post['id'])

        if parent_comments.exists():
            parent_comments = list(parent_comments)
            parent_comments = CommentSerializer(parent_comments, many=True).data
            for comment in parent_comments:
                comment['user_name'] = Users.objects.get(pk=comment['user']).username
                comment['user_avatar'] = Users.objects.get(pk=comment['user']).avatar
        else :
            parent_comments = []
        post['comments'] = parent_comments
        post['user_name'] = Users.objects.get(pk=post['user']).username
        post['user_avatar'] = Users.objects.get(pk=post['user']).avatar
        post['num_comments'] = Comment.objects.filter(post_id=post['id']).count()
        # 构造返回结果
        response_data = {
            'message': 'Success',
            'post': post
        }
        print('response_data_one_post', response_data)
        
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


def get_children_comments(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        # 处理JSON数据
        parent_id = json_data.get('parent_id', None)  # 获取JSON数据中的特定字段值
        post_id = json_data.get('post_id', None)  # 获取JSON数据中的特定字段值
        parent_search = Comment.objects.get(id=parent_id)
        post_search = Post.objects.get(id=post_id)
        children_comments = Comment.objects.filter(is_post_comment=False, parent_comment=parent_search, post=post_search)
        if children_comments.exists():
            children_comments = list(children_comments)
            children_comments = CommentSerializer(children_comments, many=True).data
            for comment in children_comments:
                comment['user_name'] = Users.objects.get(pk=comment['user']).username
                comment['user_avatar'] = Users.objects.get(pk=comment['user']).avatar
        else:
            children_comments = []
       
        # 构造返回结果
        response_data = {
            'message': 'Success',
            'children_comments': children_comments
        }
        print('response_data_comments',response_data)
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)