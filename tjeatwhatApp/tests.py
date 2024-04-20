from django.test import TestCase, Client
from django.urls import reverse
from .views import *
from .models import Post, Comment, Users
import json

class MyappTestCase(TestCase):
    def setUp(self):
        # 创建一个测试用户
        self.user = Users.objects.create(username='test_user', avatar='test@example.com')
        print(self.user.id)
        
        # 创建一个测试帖子
        self.post = Post.objects.create(user=self.user, title='Test Title', content='Test Content')

        # 创建一个测试评论
        self.comment = Comment.objects.create(is_post_comment=True, user=self.user, post=self.post, content='Test Comment', ip='上海嘉定')

        # 创建一个Django测试客户端
        self.client = Client()

    def test_post_model(self):
        print('test1')
        self.assertEqual(self.post.title, 'Test Title')
        self.assertEqual(self.post.content, 'Test Content')

    def test_comment_model(self):
        print('test2')

        self.assertTrue(self.comment.is_post_comment)
        self.assertEqual(self.comment.content, 'Test Comment')


    def test_search_posts_view(self):
        print('test3')
        # 构造POST请求数据
        data = {'content': 'Test Content'}

        # 发送POST请求
        response = self.client.post(reverse('search_posts'), json.dumps(data), content_type='application/json')

        # 检查响应状态码
        self.assertEqual(response.status_code, 200)

        # 检查响应数据
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'Success')
        self.assertTrue('posts' in response_data)

    def test_get_one_post_view(self):
        print('test4')
        # 发送GET请求
        response = self.client.get(reverse('get_one_post', kwargs={'id': self.post.id}))

        # 检查响应状态码
        self.assertEqual(response.status_code, 200)

        # 检查响应数据
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'Success')
        self.assertTrue('post' in response_data)

    def test_get_children_comments_view(self):
        print('test5')
        # 构造POST请求数据
        data = {'parent_id': self.comment.id, 'post_id': self.post.id}

        # 发送POST请求
        response = self.client.post(reverse('get_children_comments'), json.dumps(data), content_type='application/json')

        # 检查响应状态码
        self.assertEqual(response.status_code, 200)

        # 检查响应数据
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'Success')
        self.assertTrue('children_comments' in response_data)
