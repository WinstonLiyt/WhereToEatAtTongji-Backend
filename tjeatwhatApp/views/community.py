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
from ..models.communitymodels import Post, Comment, PostImages, Upvote, Star, UpvoteComment
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


def search_posts(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        content = json_data.get('content', None) 
        user_id = json_data.get('user_id', None)
        # 搜索数据库中含有message的所有帖子
        posts = Post.objects.filter(content__icontains=content)  # 大小写不敏感
        if posts.exists():
            posts = list(posts)
            serializer = PostSerializer(posts, many=True)
            serialized_posts = serializer.data
            for post in serialized_posts:
                if user_id is not None:
                    upvote = Upvote.objects.filter(post_id=post['id'], user_id=user_id).exists()
                    star = Star.objects.filter(post_id=post['id'], user_id=user_id).exists()
                    post['upvoted'] = upvote
                    post['stared'] = star
                image_urls = list(PostImages.objects.filter(post_id=post['id']).values_list('url', flat=True))
                post['images'] = image_urls
                post['num_comments'] = Comment.objects.filter(post_id=post['id']).count()
                post['user_name'] = Users.objects.get(pk=post['user']).username
                post['user_avatar'] = Users.objects.get(pk=post['user']).avatar
        else:
            posts = []
        # 将查询结果序列化为JSON格式
        # 构造返回结果
        response_data = {
            'message': 'Success',
            'posts': serialized_posts
        }
        print('response_data_posts: ', response_data)
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

def get_one_post(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        
        id = json_data.get('id', None)
        user_id = json_data.get('user_id', None)
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
                if user_id is not None:
                    upvote = UpvoteComment.objects.filter(comment_id=comment['id'], user_id=user_id).exists()
                    comment['upvoted'] = upvote
                comment['user_name'] = Users.objects.get(pk=comment['user']).username
                comment['user_avatar'] = Users.objects.get(pk=comment['user']).avatar
        else :
            parent_comments = []

        post['num_comments'] = Comment.objects.filter(post_id=post['id']).count()
        post['user_name'] = Users.objects.get(pk=post['user']).username
        post['user_avatar'] = Users.objects.get(pk=post['user']).avatar
        post['comments'] = parent_comments
        # 构造返回结果
        response_data = {
            'message': 'Success',
            'post': post
        }
        print('response_data_one_post: ', response_data)
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


def get_children_comments(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        # 处理JSON数据
        parent_id = json_data.get('parent_id', None)  # 获取JSON数据中的特定字段值
        post_id = json_data.get('post_id', None)  # 获取JSON数据中的特定字段值
        user_id = json_data.get('user_id', None)
        parent_search = Comment.objects.get(id=parent_id)
        post_search = Post.objects.get(id=post_id)
        children_comments = Comment.objects.filter(is_post_comment=False, parent_comment=parent_search, post=post_search)
        if children_comments.exists():
            children_comments = list(children_comments)
            children_comments = CommentSerializer(children_comments, many=True).data
            for comment in children_comments:
                if user_id is not None:
                    upvote = UpvoteComment.objects.filter(comment_id=comment['id'], user_id=user_id).exists()
                    comment['upvoted'] = upvote
                comment['user_name'] = Users.objects.get(pk=comment['user']).username
                comment['user_avatar'] = Users.objects.get(pk=comment['user']).avatar
        else:
            children_comments = []
       
        # 构造返回结果
        response_data = {
            'message': 'Success',
            'children_comments': children_comments
        }
        print('response_data_comments: ',response_data)
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([])
def create_post(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        # 处理JSON数据
        user_id = json_data.get('user_id')
        title = json_data.get('title')
        images = json_data.get('images', [])
        label = json_data.get('label')
        content = json_data.get('content')
        ip = json_data.get('ip')
        post = Post.objects.create(
            user_id=user_id,
            title=title,
            content=content,
            label=label,
            ip=ip
        )
        for image_url in images:
            PostImages.objects.create(
                url=image_url,
                post=post
            )
        return JsonResponse({'message': 'Success', 'time': post.time, 'id': post.id}, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)
    

# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([])
def delete_post(request):
    if request.method == 'DELETE':
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        # 检查查询参数是否存在
        post_id = json_data.get('post_id')
        user_id = json_data.get('user_id')
        if not post_id or not user_id:
            return JsonResponse({'message': 'post_id and user_id are required'}, status=400)
        try:
            post = Post.objects.get(id=post_id, user_id=user_id)
            post.delete()
            return JsonResponse({'message': 'Success'}, status=204)
        except Post.DoesNotExist:
            return JsonResponse({'message': 'Post not found or user is not authorized to delete it'}, status=404)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


# @authentication_classes([JSONWebTokenAuthentication])
def comment_post(request):
    if request.method == 'POST':
        # 检查请求体中的JSON数据
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)

        # 检查必需的参数是否存在
        post_id = json_data.get('post_id')
        user_id = json_data.get('user_id')
        content = json_data.get('content')

        if not post_id or not user_id or not content:
            return JsonResponse({'message': 'post_id, user_id, and content are required'}, status=400)

        # 检查请求头中的token参数进行身份验证（如果需要）
        token = request.headers.get('token')
        # 在这里进行身份验证和其他必要的检查

        # 创建新的评论对象并保存到数据库

        comment = Comment.objects.create(
            post_id=post_id,
            user_id=user_id,
            content=content,
        )
        user = Users.objects.get(id=user_id)
        comment_data = {
            'id': comment.id,
            'user_name': user.username,  
            'user_avatar': user.avatar,  
            'content': comment.content,
            'time': comment.time,
            'num_upvotes': comment.num_upvotes
        }

        return JsonResponse({'message': 'Success', 'comment': comment_data}, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

# @authentication_classes([JSONWebTokenAuthentication])
def reply_comment(request):
    if request.method == 'POST':
        # 检查请求体中的JSON数据
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)

        # 检查必需的参数是否存在
        parent_comment_id = json_data.get('parent_comment_id')
        user_id = json_data.get('user_id')
        content = json_data.get('content')
        ip = json_data.get('ip')

        if not parent_comment_id or not user_id or not content:
            return JsonResponse({'message': 'parent_comment_id, user_id, and content are required'}, status=400)

        # 在这里进行身份验证和其他必要的检查
        parent_comment = Comment.objects.get(id=parent_comment_id)
        # 创建新的评论对象并保存到数据库
        comment = Comment.objects.create(
            parent_comment_id=parent_comment_id,
            user_id=user_id,
            content=content,
            is_post_comment=False,
            post_id=parent_comment.post,
            ip=ip
        )
        user = Users.objects.get(id=user_id)
        # 构造评论的信息
        comment_data = {
            'id': comment.id,
            'user_name': user.username, 
            'user_avatar': user.avatar, 
            'content': comment.content,
            'time': comment.time,  
            'num_upvotes': comment.num_upvotes
        }

        # 构造返回的JSON数据
        response_data = {
            'message': 'Success',
            'comments': comment_data
        }

        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)
    
# @authentication_classes([JSONWebTokenAuthentication])
def change_post_reaction(request):
    if request.method == 'PUT':
        # 解析请求体中的JSON数据
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)

        # 获取请求体中的参数
        field = json_data.get('field')
        change = json_data.get('change')
        user_id = json_data.get('user_id')
        post_id = json_data.get('post_id')

        # 检查必需的参数
        if user_id is None or change is None:
            return JsonResponse({'message': 'user_id or change is required'}, status=400)

        # 检查可选的参数
        if field not in ['num_upvotes', 'num_stars']:
            return JsonResponse({'message': 'Invalid field'}, status=400)

        # 这里添加对用户权限的检查，确定用户是否有权限执行操作

        # 在这里执行更新帖子统计信息的操作
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({'message': 'Post not found'}, status=404)

        # 更新帖子统计信息
        if field == 'num_upvotes':
            if change:
                post.num_upvotes += 1
                Upvote.objects.create(
                    user_id=user_id,
                    post_id=post_id
                )
            else:
                post.num_upvotes -= 1
                upvote = Upvote.objects.get(user_id=user_id, post_id=post_id)
                if upvote:
                    upvote.delete()
                else:
                    return JsonResponse({'message': 'Upvote not found'}, status=404)
        elif field == 'num_stars':
            if change:
                post.num_stars += 1
                Star.objects.create(
                    user_id=user_id,
                    post_id=post_id
                )
            else:
                post.num_stars -= 1
                star = Star.objects.get(user_id=user_id, post_id=post_id)
                if star:
                    star.delete()
                else:
                    return JsonResponse({'message': 'Star not found'}, status=404)

        # 保存更新后的帖子对象
        post.save()

        # 构造返回的JSON数据
        response_data = {
            'message': 'Success',
        }
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

# @authentication_classes([JSONWebTokenAuthentication])
def delete_comment(request):
    if request.method == 'DELETE':
        # 获取查询参数
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        
        comment_id = json_data.get('id')
        comment = Comment.objects.get(id=comment_id)
        if comment:
            comment.delete()
        else:
            return JsonResponse({'message': 'Comment not found'}, status=404)
        # 构造返回的JSON数据
        response_data = {
            'message': 'Success'
        }

        return JsonResponse(response_data, status=204)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

# @authentication_classes([JSONWebTokenAuthentication])
def change_comment_reaction(request):
    if request.method == 'PUT':
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        
        change = json_data.get('change')
        user_id = json_data.get('user_id')
        comment_id = json_data.get('comment_id')

        # 检查必需的参数
        if comment_id is None or change is None :
            return JsonResponse({'message': 'comment_id or change is required'}, status=400)
      
        # 这里添加对用户权限的检查，确定用户是否有权限执行操作

        # 在这里执行更新评论的操作
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return JsonResponse({'message': 'Comment not found'}, status=404)

        # 更新评论的点赞数
        if change:
            comment.num_upvotes += 1
            UpvoteComment.objects.create(
                user_id=user_id,
                comment_id=comment_id
            )
        else:
            comment.num_upvotes -= 1
            upvote = UpvoteComment.objects.get(user_id=user_id, comment_id=comment_id)
            if upvote:
                upvote.delete()
            else:
                return JsonResponse({'message': 'Upvote not found'}, status=404)

        # 保存更新后的评论对象
        comment.save()

        # 构造返回的JSON数据
        response_data = {
            'message': 'Success',
            'permitted': comment.num_upvotes
        }

        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)