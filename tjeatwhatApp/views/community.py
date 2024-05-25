import django
from django.utils.encoding import smart_str
django.utils.encoding.smart_text = smart_str
from django.conf import settings
import os
from django.utils.translation import gettext
django.utils.translation.ugettext = gettext
from uuid import uuid4
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tjeatwhatApp.extensions.auth import JwtQueryParamsAuthentication,EmptyParamsAuthentication
# from rest_framework.decorators import authentication_classes, permission_classes
from ..models.communitymodels import Post, Comment, PostImages, Upvote, Star, UpvoteComment, Message
from ..models.usermodels import User
from rest_framework import serializers
from rest_framework.decorators import api_view, authentication_classes

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'  

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

@api_view(['POST'])
@authentication_classes([EmptyParamsAuthentication])
def search_posts(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        print(json_data)
        content = json_data.get('content', None) 
        user_id = None
        print('user:', request.user, type(request.user))
        if request.user['id'] is not None:
            user_id = request.user['id']
        else:
            user_id = None
        print('user:', user_id)
        # 搜索数据库中含有content的所有帖子
        posts = Post.objects.filter(title__icontains=content)  # 大小写不敏感
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
                is_user = True if user_id == post['user'] else False
                post['is_user'] = is_user
                image_urls = list(PostImages.objects.filter(post_id=post['id']).values_list('url', flat=True))
                post['images'] = image_urls
                post['num_comments'] = Comment.objects.filter(post_id=post['id']).count()
                post['user_name'] = User.objects.get(pk=post['user']).nickname
                post['user_avatar'] = User.objects.get(pk=post['user']).avatar_url
        else:
            serialized_posts = []
        # 将查询结果序列化为JSON格式
        # 构造返回结果
        response_data = {
            'message': 'Success',
            'posts': list(reversed(serialized_posts))
        }
        # print('response_data_posts: ', response_data)
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

@api_view(['POST'])
def get_one_post(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        print("json_data", json_data)
        id = json_data.get('id', None)
        print("id:", id)
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return JsonResponse({'message': 'Post not found'}, status=404)
        post = PostSerializer(post).data
        parent_comments = Comment.objects.filter(is_post_comment=True, post_id=post['id'])

        if parent_comments.exists():
            parent_comments = [comment.id for comment in parent_comments]
        else :
            parent_comments = []
        post['images'] = list(PostImages.objects.filter(post_id=post['id']).values_list('url', flat=True))
        post['num_comments'] = Comment.objects.filter(post_id=post['id']).count()
        post['user_name'] = User.objects.get(pk=post['user']).nickname
        post['user_avatar'] = User.objects.get(pk=post['user']).avatar_url
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

@api_view(['POST'])
@authentication_classes([EmptyParamsAuthentication])
def get_one_comment(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        # 处理JSON数据
        id = json_data.get('id', None)  # 获取JSON数据中的特定字段值
        user_id = None
        if request.user['id'] is not None:
            user_id = request.user['id']
        else:
            user_id = None
        print('id:',id)
        comment_search = Comment.objects.get(id=id)
        if comment_search is not None:
            comment_search = CommentSerializer(comment_search).data
            children_comments = Comment.objects.filter(parent_comment_id=comment_search['id'])
            if children_comments.exists():
                children_comments = [comment.id for comment in children_comments]
            else:
                children_comments = []
            comment_search['children_ids'] = children_comments
            if user_id is not None:
                upvote = UpvoteComment.objects.filter(comment_id=comment_search['id'], user_id=user_id).exists()
                comment_search['upvoted'] = upvote
            comment_search['user_name'] = User.objects.get(pk=comment_search['user']).nickname
            comment_search['user_avatar'] = User.objects.get(pk=comment_search['user']).avatar_url
            comment_search['is_user'] = comment_search['user'] == user_id
        else:
            return JsonResponse({'message': 'Comment not found'}, status=404)
       
        # 构造返回结果
        response_data = {
            'message': 'Success',
            'comments': comment_search
        }
        print('response_data_comments: ',response_data)
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

@api_view(['POST'])
@authentication_classes([JwtQueryParamsAuthentication])
def create_post(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        # 处理JSON数据
        print('json_data: ',json_data)
        user_id = request.user.get('id')
        title = json_data.get('title')
        images = json_data.get('images', [])
        label = json_data.get('label')
        content = json_data.get('content')
        ip = json_data.get('ip')
        user = User.objects.get(id=user_id)
        user.credits += 50
        user.save()
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
    
@api_view(['DELETE'])
@authentication_classes([JwtQueryParamsAuthentication])
def delete_post(request):
    if request.method == 'DELETE':
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        # 检查查询参数是否存在
        post_id = json_data.get('post_id')
        user_id = request.user.get('id')

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

@api_view(['POST'])
@authentication_classes([JwtQueryParamsAuthentication])
def comment_post(request):
    if request.method == 'POST':
        # 检查请求体中的JSON数据
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        # 检查必需的参数是否存在
        post_id = json_data.get('post_id')
        user_id = request.user.get('id')
        content = json_data.get('content')

        if not post_id or not user_id or not content:
            return JsonResponse({'message': 'post_id, user_id, and content are required'}, status=400)

        user = User.objects.get(id=user_id)
        user.credits += 10
        user.save()
        # 创建新的评论对象并保存到数据库


        comment = Comment.objects.create(
            post_id=post_id,
            user_id=user_id,
            content=content,
        )

        # 待测试
        Message.objects.create(
            category=2,
            replier_id=user_id,
            receiver_id=Post.objects.get(id=post_id).user_id
        )

        user = User.objects.get(id=user_id)
        comment_data = {
            'id': comment.id,
            'user_name': user.nickname,  
            'user_avatar': user.avatar_url,  
            'content': comment.content,
            'time': comment.time,
            'num_upvotes': comment.num_upvotes
        }

        return JsonResponse({'message': 'Success', 'comment': comment_data}, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

@api_view(['POST'])
@authentication_classes([JwtQueryParamsAuthentication])
def reply_comment(request):
    if request.method == 'POST':
        # 检查请求体中的JSON数据
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)

        # 检查必需的参数是否存在
        parent_comment_id = json_data.get('parent_comment_id')
        user_id = request.user.get('id')
        replied_id = json_data.get('replied_id')
        content = json_data.get('content')
        user = User.objects.get(id=user_id)
        user.credits += 5
        user.save()

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
            post_id=parent_comment.post_id,
        )

        # 待测试
        Message.objects.create(
            category=2,
            replier_id=user_id,
            receiver_id=replied_id
        )

        user = User.objects.get(id=user_id)
        # 构造评论的信息
        comment_data = {
            'id': comment.id,
            'user_name': user.nickname, 
            'user_avatar': user.avatar_url, 
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

@api_view(['PUT'])
@authentication_classes([JwtQueryParamsAuthentication])
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
        user_id = request.user.get('id')
        post_id = json_data.get('post_id')

        # 检查必需的参数
        if user_id is None or change is None:
            return JsonResponse({'message': 'user_id or change is required'}, status=400)

        # 检查可选的参数
        if field not in ['num_upvotes', 'num_stars']:
            return JsonResponse({'message': 'Invalid field'}, status=400)

        # 在这里执行更新帖子统计信息的操作
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({'message': 'Post not found'}, status=404)
        print(json_data)
        # 更新帖子统计信息
        if field == 'num_upvotes':
            if change:
                user = User.objects.get(id=user_id)
                user.credits += 5
                user.save()
                post.num_upvotes += 1
                Upvote.objects.create(
                    user_id=user_id,
                    post_id=post_id
                )
                # 待测试
                Message.objects.create(
                    category=0,
                    replier_id=user_id,
                    receiver_id=Post.objects.get(id=post_id).user_id
                )
            else:
                post.num_upvotes -= 1
                upvote = Upvote.objects.get(user_id=user_id, post_id=post_id)
                # 待测试
                notifications = Message.objects.filter(category=0,replier_id=user_id,receiver_id=Post.objects.get(id=post_id).user_id)
                if notifications.exists():
                    notifications.first().delete()
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
                # 待测试
                Message.objects.create(
                    category=1,
                    replier_id=user_id,
                    receiver_id=Post.objects.get(id=post_id).user_id
                )
            else:
                post.num_stars -= 1
                star = Star.objects.get(user_id=user_id, post_id=post_id)
                # 待测试
                notifications = Message.objects.filter(category=1,replier_id=user_id,receiver_id=Post.objects.get(id=post_id).user_id)
                if notifications.exists():
                    notifications.first().delete()
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

@api_view(['DELETE'])
@authentication_classes([JwtQueryParamsAuthentication])
def delete_comment(request):
    if request.method == 'DELETE':
        # 获取查询参数
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        replied_id = json_data.get('replied_id')
        comment_id = json_data.get('id')
        comment = Comment.objects.get(id=comment_id)
        if comment:
            comment.delete()
        else:
            return JsonResponse({'message': 'Comment not found'}, status=404)
        # 待测试
        notifications = Message.objects.filter(category=2,replier_id=request.user.get('id'),receiver_id=replied_id)
        if notifications.exists():
            notifications.first().delete()

        # 构造返回的JSON数据
        response_data = {
            'message': 'Success'
        }

        return JsonResponse(response_data, status=204)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

@api_view(['PUT'])
@authentication_classes([JwtQueryParamsAuthentication])
def change_comment_reaction(request):
    if request.method == 'PUT':
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            print('Invalid JSON data')
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        print(json_data)
        change = json_data.get('change')
        user_id = request.user.get('id')
        comment_id = json_data.get('comment_id')
        # 检查必需的参数
        if comment_id is None or change is None :
            print('comment_id or change is required')
            return JsonResponse({'message': 'comment_id or change is required'}, status=400)
      
        # 在这里执行更新评论的操作
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return JsonResponse({'message': 'Comment not found'}, status=404)

        # 更新评论的点赞数
        if change:
            user = User.objects.get(id=user_id)
            user.credits += 2
            user.save()
            comment.num_upvotes += 1
            UpvoteComment.objects.create(
                user_id=user_id,
                comment_id=comment_id
            )
            # 待测试
            Message.objects.create(
                category=0,
                replier_id=user_id,
                receiver_id=Comment.objects.get(id=comment_id).user_id
            )

        else:
            comment.num_upvotes -= 1
            upvote = UpvoteComment.objects.get(user_id=user_id, comment_id=comment_id)
            # 待测试
            notifications = Message.objects.filter(category=0,replier_id=user_id,receiver_id=Comment.objects.get(id=comment_id).user_id)
            if notifications.exists():
                notifications.first().delete()
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


@api_view(['GET'])
@authentication_classes([JwtQueryParamsAuthentication])
def load_msg(request):
    if request.method == 'GET':
        user_id = request.user.get('id')
        # 待测试
        notifications = Message.objects.filter(receiver_id=user_id)
        if notifications.exists():
            notifications = MessageSerializer(list(notifications)).data
            for notification in notifications:
                if notification.replier_id is not None:
                    notification['user_name'] = User.objects.get(id=notification['replier']).nickname
                    notification['user_avatar'] = User.objects.get(id=notification['replier']).avatar_url
        else:
            notifications = []
        response_data = {
            'message': 'Success',
            'notifications': list(notifications)
        }
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

@api_view(['DELETE'])
@authentication_classes([JwtQueryParamsAuthentication])
def delete_msg(request):
    if request.method == 'DELETE':
        user_id = request.user.get('id')
        # 待测试
        notifications = Message.objects.filter(receiver_id=user_id)
        if notifications.exists():
            notifications.delete()
            return JsonResponse({'message': 'Success'}, status=204)
        else:
            return JsonResponse({'message': 'Messages not found'}, status=404)
        
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

