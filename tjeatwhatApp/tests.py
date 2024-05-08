from django.test import TestCase, Client
from .models.usermodels import User
from tjeatwhatApp.utils.jwt_auth import create_token
from rest_framework import status
from django.urls import reverse
import json
# Create your tests here.
class StudentTestCase(TestCase):
    """
    def setUp(self)：用来初始化环境，包括创建初始数据，或做一些其他准备工作
    def test_xxx(self)：xxx可以是任何东西，以test_开头的方法，都会被django认为是需要测试的方法，跑测试时会被执行。
        注：每个需要被测试的方法都是相互独立的
    def tearDown(self)：跟setUp相对，用来清理测试环境和测试数据（在django中可以不关心这个）
    """
    def setUp(self):
        # print('setUp')
        self.user=User.objects.create(
            username='stu1',
            phone='111',
            email='test1@qq.com',
            password='333'
        )
        # print("userid:",self.user.id)
        self.token=create_token({'user_id': self.user.id, 'username': self.user.username})
        # 创建一个 Django 测试客户端
        self.client = Client()

    def test_user_model(self):
        print('\n')
        print('test1:测试用户创建')
        self.assertEqual(self.user.username, 'stu1')
        self.assertEqual(self.user.phone, '111')
        self.assertEqual(self.user.email, 'test1@qq.com')
        print('\n')

    def test_login(self):
        print('\n')
        print("test2:测试token生成")
        # 构造 POST 请求数据
        data = {
            'name': 'stu1',
            'password': '333'
        }
        self.assertEqual(self.user.username, 'stu1')
        self.assertEqual(self.user.password, '333')
        # 发送 POST 请求
        response = self.client.post(reverse('UserLogin'), data, format='json')
        # 检查响应状态码是否为 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 检查响应数据中是否包含预期的内容
        self.assertIn('token', response.data)
        print('\n')

    def test_no_token(self):
        print('\n')
        print("test3:发送没有 Token 的 GET 请求")
        
        # 发送没有 Token 的 GET 请求
        response = self.client.get(reverse('TestTokenView'))
        print("response data:",response.data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['code'], 1003)
        # self.assertEqual(response.data['error'], 'token认证失败')
         # 将响应数据转换为字典
        response_data = json.loads(response.content)
        
        # 检查返回的字典是否符合预期
        self.assertEqual(response_data['code'], '1003')
        self.assertEqual(response_data['error'], 'token认证失败')
        print('\n')

    def test_invalid_token(self):
        print('\n')
        print("test4:使用无效 Token 发送 GET 请求")
        
        # 使用无效 Token 发送 GET 请求
        invalid_token = 'invalid_token'
        url = reverse('TestTokenView') + '?token=' + invalid_token
        response = self.client.get(url)
        response_data = json.loads(response.content)
        
        # 检查返回的字典是否符合预期
        self.assertEqual(response_data['code'], '1003')
        self.assertEqual(response_data['error'], 'token认证失败')
        print('\n')

    def test_valid_token(self):

        print('\n')
        print("test5:使用有效 Token 发送 GET 请求")
        data = {
            'name': 'stu1',
            'password': '333'
        }
        self.assertEqual(self.user.username, 'stu1')
        self.assertEqual(self.user.password, '333')
        # 发送 POST 请求
        response = self.client.post(reverse('UserLogin'), data, format='json')
        token = self.token
        # 使用有效 Token 发送 GET 请求
        url = reverse('TestTokenView') + '?token=' + token
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, '成功获取信息')
        print('\n')
