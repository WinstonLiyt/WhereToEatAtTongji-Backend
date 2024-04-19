# 修一些报错
import django
from django.utils.encoding import smart_str
django.utils.encoding.smart_text = smart_str
from django.utils.translation import gettext
django.utils.translation.ugettext = gettext

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
        message = request.POST.get('message', '')
        
        # 进行JWT验证
        try:
            user = User.objects.get(pk=request.user.id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=400)
        
        # 搜索数据库中含有message的所有帖子
        posts = Post.objects.filter(content__icontains=message)  # 大小写不敏感
        posts = list(posts)

        # 将查询结果序列化为JSON格式
        serialized_posts = PostSerializer(posts, many=True)
        
        # 构造返回结果
        response_data = {
            'message': 'Success',
            'posts': serialized_posts.data
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
    pass