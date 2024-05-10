from django.test import TestCase, Client
from rest_framework.test import APIClient
from .models.usermodels import User
from .models.restaurantmodels import Restaurant,RestImage,RestTag
from .models.dishmodels import Dish,DishTag,DishEval
from tjeatwhatApp.utils.jwt_auth import create_token
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
import json
from datetime import datetime

class GXTestCase1(TestCase):
    def setUp(self): 
    # 创建一个测试用户 
        self.user=User.objects.create(openid='666',wx_nickname ='sb',wx_avatar_url = 'xxx',type = 1,credits=0,token = 1)
        self.tag1=DishTag.objects.create(name='焦糖')
        self.tag2=DishTag.objects.create(name='快乐水')
        self.tag3=RestTag.objects.create(name='火锅')
        self.tag4=RestTag.objects.create(name='小吃')
        self.rest_image=RestImage.objects.create(image='test_iamge.jpg')
        self.rest_image1=RestImage.objects.create(image='test_iamge1.jpg')

        self.rest=Restaurant.objects.create(name='啦啦啦',owner=self.user,location='B楼',description='太酷了',phone_number='456789')
        self.dish=Dish.objects.create(name='可乐',description='牛',image='test_iamge.jpg',price=5.2,restaurant=self.rest)
        self.dish.tags.set([self.tag1,self.tag2])
        self.rest.tags.set([self.tag3,self.tag4])
        self.rest.images.set([self.rest_image,self.rest_image1])
       
        # 创建一个Django测试客户端 
        self.client = Client() 
        self.upload_url = reverse('upload_image')  # 获取上传图片的 URL
    
    def test_upload_file(self):
        print()  
        print('test1:upload_file') 
        local_image_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
        
        # 打开本地图片文件
        with open(local_image_path, 'rb') as f:
            # 创建上传文件对象
            image_file = SimpleUploadedFile("test_image.jpg", f.read(), content_type="image/jpeg")
        
        # 发送 POST 请求上传图片
        response = self.client.post(self.upload_url, {'file': image_file})
        response_data = json.loads(response.content) 
        print(response_data)
        self.assertEqual(response.status_code, 200)
        
    
    def test_create_restaurant(self):
        print()  
        print('test2:create_rest') 
        data = {'name': 'test_rest',
                'location':'安楼',
                'description': None,
                'images':['test_image.jpg','test_image1.jpg'],
                'tags':['垃圾'],
                'phone_number':'123456'
                } 
        # 发送POST请求 
        response = self.client.post(reverse('create_restaurant',kwargs={'user_id':self.user.id}), json.dumps(data), content_type='application/json')
        response_data = json.loads(response.content) 
        print(response_data['time'])
        self.Rest_id=response_data['id']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Restaurant.objects.filter(location='安楼').exists())
        
        
    

    def test_delete_restaurant(self):
        print()  
        print('test3:delete_restaurant') 
        self.assertTrue(Restaurant.objects.filter(name='啦啦啦').exists()) 
        response = self.client.delete(reverse('delete_restaurant',kwargs={'rest_id':self.rest.id}))
        response_data = json.loads(response.content) 
        print(response_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Restaurant.objects.filter(name='啦啦啦').exists()) 
    
    def test_create_dish(self):
        print()  
        print('test4:create_dish') 
        data = {'name': '汉堡',
                'description': '难吃',
                'tags':['优惠','必点','神奇'],
                'image':'test_image.jpg',
                'price':14
                } 
        # 发送POST请求 
        response = self.client.post(reverse('create_dish',kwargs={'rest_id':self.rest.id}), json.dumps(data), content_type='application/json')
        response_data = json.loads(response.content) 
        print(response_data['time'])
        self.Dish_id=response_data['id']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Dish.objects.filter(name='汉堡').exists()) 
    
    
    def test_delete_dish(self):
        print()  
        print('test5:delete_dish') 
        self.assertTrue(Dish.objects.filter(name='可乐').exists()) 
        response = self.client.delete(reverse('delete_dish',kwargs={'dish_id':self.dish.id}))
        response_data = json.loads(response.content) 
        print(response_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Dish.objects.filter(name='可乐').exists()) 



class GXTestCase2(TestCase):
    def setUp(self): 
    # 创建一个测试用户 

        self.user=User.objects.create(openid='666',wx_nickname ='sb',wx_avatar_url = 'xxx',type = 1,credits=0,token = 1)
        self.tag1=DishTag.objects.create(name='焦糖')
        self.tag2=DishTag.objects.create(name='快乐水')
        self.tag3=RestTag.objects.create(name='火锅')
        self.tag4=RestTag.objects.create(name='小吃')
        self.rest_image=RestImage.objects.create(image='test_iamge.jpg')
        self.rest_image1=RestImage.objects.create(image='test_iamge1.jpg')

        self.rest=Restaurant.objects.create(name='啦啦啦',location='B楼',description='太酷了',phone_number='456789',owner=self.user)
        self.dish=Dish.objects.create(name='可乐',description='牛',image='test_iamge.jpg',price=5.2,restaurant=self.rest)
        self.dish.tags.set([self.tag1,self.tag2])
        self.rest.tags.set([self.tag3,self.tag4])
        self.rest.images.set([self.rest_image,self.rest_image1])
        # 创建一个Django测试客户端 
        self.client = Client() 
    
        
    
    def test_update_restaurant(self):
        print()  
        print('test6:update_rest') 
        # 构造POST请求数据 
        data = {'name': 'KFC',
                'description': '疯狂星期四',
                'images':['test_image1.jpg','test_image2.jpg'],
                } 
        # 发送POST请求 
        response = self.client.put(reverse('update_restaurant',kwargs={'rest_id':self.rest.id}), json.dumps(data), content_type='application/json')
        response_data = json.loads(response.content) 
        print(response_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Restaurant.objects.filter(name='KFC').exists())
        
    
    def test_update_dish(self):
        print()  
        print('test7:update_dish') 
        # 构造POST请求数据 
        data = {'price': 12.3,
                'tags':['美味','必点']
                } 
        # 发送POST请求 
        response = self.client.put(reverse('update_dish',kwargs={'dish_id':self.dish.id}), json.dumps(data), content_type='application/json')
        response_data = json.loads(response.content) 
        print(response_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(DishTag.objects.filter(name='美味').exists()) 


class GXTestCase3(TestCase):
    # 创建一个测试用户 
    def setUp(self):
        self.user=User.objects.create(openid='666',wx_nickname ='sb',wx_avatar_url = 'xxx',type = 1,credits=0,token = 1)
        self.user1=User.objects.create(openid='777',wx_nickname ='def',wx_avatar_url = 'xxx',type = 1,credits=0,token = 1)
        
        self.tag1=DishTag.objects.create(name='焦糖')
        self.tag2=DishTag.objects.create(name='快乐水')
        self.tag3=RestTag.objects.create(name='火锅')
        self.tag4=RestTag.objects.create(name='小吃')
        self.rest_image=RestImage.objects.create(image='test_iamge.jpg')
        self.rest_image1=RestImage.objects.create(image='test_iamge1.jpg')

        self.rest=Restaurant.objects.create(name='饮料店',owner=self.user,location='B楼',description='太酷了',phone_number='456789')
        self.dish=Dish.objects.create(name='可乐',description='牛',image='test_iamge.jpg',price=5.2,restaurant=self.rest)
        self.dish.tags.set([self.tag1,self.tag2])
        self.rest.tags.set([self.tag3,self.tag4])
        self.rest.images.set([self.rest_image,self.rest_image1])

        self.dish_eval=DishEval.objects.create(score=5,dish=self.dish,user=self.user,comment='非常棒',
                                               time=datetime.now())

        self.tag5=DishTag.objects.create(name='辣品')
        self.tag6=DishTag.objects.create(name='垃圾食品')
        self.tag7=RestTag.objects.create(name='der')
        self.tag8=RestTag.objects.create(name='fr')
        self.rest_image2=RestImage.objects.create(image='test_iamge2.jpg')
        self.rest_image3=RestImage.objects.create(image='test_iamge3.jpg')
        self.rest1=Restaurant.objects.create(name='零食',owner=self.user1,location='A楼',description='好吃',phone_number='123456')
        self.dish1=Dish.objects.create(name='可乐',description='牛',image='test_iamge.jpg',price=5.2,restaurant=self.rest)
        self.dish1.tags.set([self.tag1,self.tag2])
        self.rest1.tags.set([self.tag3,self.tag4])
        self.rest1.images.set([self.rest_image2,self.rest_image3])
        self.dish_eval1=DishEval.objects.create(score=1,dish=self.dish1,user=self.user,comment='非常差',
                                               time=datetime.now(),reply='evvw',reply_time=datetime.now())


       
        # 创建一个Django测试客户端 
        self.client = Client() 
        self.upload_url = reverse('upload_image')  # 获取上传图片的 URL 

    def test_get_all_dish(self):
        print()  
        print('test8:get_all_dish') 
        response = self.client.get(reverse('get_all_dish',kwargs={'rest_id':self.rest.id}), content_type='application/json')
        response_data = json.loads(response.content) 
        print(response_data)
        self.assertEqual(response.status_code, 200)
        return
    
    def test_get_all_dish_eval(self):
        print()  
        print('test9:get_dish_eval') 
        response = self.client.get(reverse('get_dish_eval',kwargs={'dish_id':self.dish.id}), content_type='application/json')
        response_data = json.loads(response.content) 
        print(response_data)
        self.assertEqual(response.status_code, 200)
        return
    
    def test_get_all_rest(self):
        print()  
        print('test10:get_all_dish') 
        response = self.client.get(reverse('get_all_rest'), content_type='application/json')
        response_data = json.loads(response.content) 
        print(response_data)
        self.assertEqual(response.status_code, 200)
        return

    
    
    def test_search_dish(self):
        print()  
        print('test11:search') 
        response = self.client.get(reverse('search',kwargs={'name':'可乐'}), content_type='application/json')
        response_data = json.loads(response.content) 
        print(response_data)
        # encoding=utf-8


          
        self.assertEqual(response.status_code, 200)
        return 
    
    

    def test_create_eval(self):
        print()  
        print('test12:create_eval') 
        data = {'score': 4,
                'comment': '难吃',
                } 
        # 发送POST请求 
        response = self.client.post(reverse('create_dish_eval',kwargs={'user_id':self.user.id,'dish_id':self.dish.id}), json.dumps(data), content_type='application/json')
        response_data = json.loads(response.content) 
        print(response_data['time'])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(DishEval.objects.get(pk=response_data['id']).score==4) 
        return
    

    def test_delete_eval(self):
        print()  
        print('test13:delete_dish_eval') 
        self.assertTrue(DishEval.objects.filter(comment='非常差').exists()) 
        response = self.client.delete(reverse('delete_dish_eval',kwargs={'eval_id':self.dish_eval1.id}))
        response_data = json.loads(response.content) 
        print(response_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(DishEval.objects.filter(comment='非常差').exists()) 
        return 
    
    def test_reply_eval(self):
        print()  
        print('test14:reply_eval') 
        data = {'reply': '你说的不对',
                } 
        # 发送POST请求 
        response = self.client.post(reverse('reply',kwargs={'eval_id':self.dish_eval.id}), json.dumps(data), content_type='application/json')
        response_data = json.loads(response.content) 
        self.assertEqual(response.status_code, 200)
        print(DishEval.objects.get(pk=self.dish_eval.id))

        return 
    
    def test_get_rest(self):
        print()  
        print('test15:get_rest') 
        response = self.client.get(reverse('get_rest',kwargs={'rest_id':self.rest.id}), content_type='application/json')
        response_data = json.loads(response.content) 
        print(response_data)
        self.assertEqual(response.status_code, 200)
        return 
    
    def test_get_dish(self):
        print()  
        print('test16:get_dish') 
        response = self.client.get(reverse('get_dish',kwargs={'dish_id':self.dish1.id}), content_type='application/json')
        response_data = json.loads(response.content) 
        print(response_data)
        self.assertEqual(response.status_code, 200)
        return 








class RecommendTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(openid='666',nickname ='abc',avatar_url = 'xxx',type = 1,credits=0,token = 1)
        self.user2=User.objects.create(openid='777',nickname ='sb',avatar_url = 'xxx',type = 1,credits=0,token = 1)
        self.user3=User.objects.create(openid='888',nickname ='def',avatar_url = 'xxx',type = 1,credits=0,token = 1)

        self.token=create_token({'id': self.user.id,'openid': self.user.openid})
        self.token2=create_token({'id': self.user2.id,'openid': self.user2.openid})
        self.token3=create_token({'id': self.user3.id,'openid': self.user3.openid})
        # 创建一个菜品标签
        self.tag1 = DishTag.objects.create(name='烧烤')
        self.tag2 = DishTag.objects.create(name='火锅')
        self.tag3=DishTag.objects.create(name='焦糖')
        self.tag4=DishTag.objects.create(name='快乐水')
        

        self.rest_image1=RestImage.objects.create(image='test_image.jpg')
        self.rest_image2=RestImage.objects.create(image='test_image.jpg')

        # 创建一些用于测试的样本餐厅
        self.restaurant1=Restaurant.objects.create(name='餐厅1', owner=self.user,location='地址1', phone_number='1234567890',description='Description1')
        self.restaurant2=Restaurant.objects.create(name='餐厅2', owner=self.user,location='地址2', phone_number='0987654321',description='Description2')
        self.restaurant3=Restaurant.objects.create(name='饮料店',owner=self.user,location='B楼',description='太酷了',phone_number='456789')
        self.restaurant1.images.set([self.rest_image1])
        self.restaurant2.images.set([self.rest_image2])
        self.restaurant3.images.set([self.rest_image1])

        self.dish1 = Dish.objects.create(name='烧烤', description='dishDescription 1', price=10.50, restaurant=self.restaurant1,image='test_image.jpg')
        self.dish2 = Dish.objects.create(name='火锅', description='dishDescription 2', price=15.75, restaurant=self.restaurant1,image='test_image.jpg')
        self.dish3 = Dish.objects.create(name='羊肉串', description='dishDescription 2', price=15.75, restaurant=self.restaurant1,image='test_image.jpg')
        self.dish4 = Dish.objects.create(name='牛肉串', description='dishDescription 2', price=15.75, restaurant=self.restaurant1,image='test_image.jpg')
        
        self.dish5 = Dish.objects.create(name='可乐', description='dishDescription 2', price=15.75, restaurant=self.restaurant3,image='test_image.jpg')
        self.dish6 = Dish.objects.create(name='雪碧', description='dishDescription 2', price=15.75, restaurant=self.restaurant3,image='test_image.jpg')
        self.dish7 = Dish.objects.create(name='盐汽水', description='dishDescription 2', price=15.75, restaurant=self.restaurant3,image='test_image.jpg')

        self.dish1.tags.add(self.tag1)
        self.dish2.tags.add(self.tag2)
        self.dish3.tags.add(self.tag1)
        self.dish4.tags.add(self.tag1)
        self.dish5.tags.add(self.tag4)
        self.dish6.tags.add(self.tag4)
        self.dish7.tags.add(self.tag4)

        self.dish_eval1=DishEval.objects.create(score=5,dish=self.dish5,user=self.user2,comment='非常棒',time=datetime.now())
        self.dish_eval1=DishEval.objects.create(score=5,dish=self.dish4,user=self.user2,comment='非常棒bang',time=datetime.now())
        self.dish_eval2=DishEval.objects.create(score=1,dish=self.dish3,user=self.user2,comment='非常差',time=datetime.now())



        self.url1 = reverse('get_all_store')  # 假设您已经正确设置了URL模式名称
        self.url2 = reverse('getAllDishByStoreID', kwargs={'store_id': self.restaurant1.id})
        self.url3 = reverse('get_dish_by_user_interest')
        

    def test_get_all_store(self):
        print("test1:随机推荐中获取所有餐厅***********************")
        # 发送 POST 请求
        token = self.token
        # 设置请求头
        headers = {'HTTP_AUTHORIZATION': token}
        response = self.client.get(self.url1,**headers)
        stores = Restaurant.objects.all()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['stores']), len(stores))

        for index, store_data in enumerate(response.data['stores']):
            self.assertEqual(store_data['id'], stores[index].id)
            self.assertEqual(store_data['name'], stores[index].name)
            #print("id=",store_data['id'])
            #print("name=",store_data['name'])
        print("response.data:",response.data,'\n')
        print('\n')

    def test_get_all_dish_with_storeid(self):
        print("test2:根据餐厅id获取所有菜品***********************")
        # data = {'store_id': self.restaurant1.id}
        # 发送 POST 请求
        token = self.token
        # 设置请求头
        headers = {'HTTP_AUTHORIZATION': token}
        response = self.client.get(self.url2,**headers)
        dishes = Dish.objects.filter(restaurant_id=self.restaurant1.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 检查返回的数据是否与数据库中的数据匹配
        self.assertEqual(len(response.data['dishes']), dishes.count())
        for index, dish_data in enumerate(response.data['dishes']):
            self.assertEqual(dish_data['id'], dishes[index].id)
            self.assertEqual(dish_data['name'], dishes[index].name)
        
        print("response.data:",response.data,'\n')
        print('\n')

    def test_get_dish_by_personalinterest(self):
        print("test5:根据个人兴趣获取菜品***********************")
        # 发送 POST 请求
        token = self.token2
        # 设置请求头
        headers = {'HTTP_AUTHORIZATION': token}
        response = self.client.get(self.url3,**headers)
        print("response.data:",response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('\n')
        



#用户访问数据测试
class UserTestCase(TestCase):
    def setUp(self):
        self.client =APIClient()
        self.user = User.objects.create(
            openid='666',
            type=1
        )
        self.token=create_token({'id': self.user.id,'openid': self.user.openid})
        self.rest_image=RestImage.objects.create(image='test_image.jpg')
        self.rest_image1=RestImage.objects.create(image='test_image.jpg')
    def test_set_username_success(self):
        print("test10:设置用户名***********************")
        url = reverse('set_name')
        # 准备POST请求的数据
        data = {
            'nickname': 'newname',
        }
        # 发送 POST 请求
        token = self.token
        # 设置请求头
        headers = {'HTTP_AUTHORIZATION': token}
        response = self.client.post(url, data,  **headers)
        # 断言响应状态码为200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 断言响应数据中包含成功修改用户名的消息
        self.assertIn('成功修改用户名', response.data['msg'])
        self.user.refresh_from_db()
        print(self.user.nickname)
        self.assertEqual(self.user.nickname, 'newname')
        print('\n')

    def test_set_avatar_success(self):
        print("test11:设置头像***********************")
        url = reverse('set_avatar')
        # 准备POST请求的数据
        data = {
            'avatar_url': 'newavatar',
        }
        # 发送 POST 请求
        token = self.token
        # 设置请求头
        headers = {'HTTP_AUTHORIZATION': token}
        response = self.client.post(url, data,  **headers)
        # 断言响应状态码为200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 断言响应数据中包含成功修改用户名的消息
        self.assertIn('成功修改头像', response.data['msg'])
        self.user.refresh_from_db()
        #print(self.user.nickname)
        self.assertEqual(self.user.avatar_url, 'newavatar')
        print('\n')

    @patch('tjeatwhatApp.views.user.WXAPPAPI')  # 模拟WXAPPAPI类
    def test_weixin_login_success(self,MockWXAPPAPI):
        print("test6:微信登录成功***********************")

        # 模拟WXAPPAPI对象的exchange_code_for_session_key方法返回的session_info
        mock_session_info = {'openid': '666'}
        MockWXAPPAPI.return_value.exchange_code_for_session_key.return_value = mock_session_info
        #MockWXAPPAPI.return_value.exchange_code_for_session_key.assert_called_once_with('mock_code')
        url=reverse('login')
        data = {'code': 'mock_code'}
        response = self.client.post(url, data, format='json')
        print("response.data:",response.data)
        # 断言响应状态码为200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #相应数据中role为1
        self.assertEqual(response.data['role'],1)
        # 断言响应数据中包含token和code为200
        self.assertIn('token', response.data)
        
    @patch('tjeatwhatApp.views.user.WXAPPAPI')  # 模拟WXAPPAPI类
    def test_student_register_success(self, MockWXAPPAPI):
        print("test9:学生注册**********")
        # 模拟WXAPPAPI对象的exchange_code_for_session_key方法返回的session_info
        mock_session_info = {'openid': 'mock_openid'}
        MockWXAPPAPI.return_value.exchange_code_for_session_key.return_value = mock_session_info

        # 设置请求URL
        url = reverse('student_register')
        
        # 准备POST请求的数据
        data = {
            'code': 'mock_code',
            'name': 'mock_name',
            'avatar_url': 1
            # 根据需要设置其他字段
        }

        # 发送POST请求
        response = self.client.post(url, data, format='json')

        # 断言响应状态码为200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 断言响应数据中包含token和code为200
        self.assertIn('token', response.data)
        self.assertEqual(response.data['code'], 200)

        print('\n')

    @patch('tjeatwhatApp.views.user.WXAPPAPI')  # 模拟WXAPPAPI类
    def test_store_register_success(self, MockWXAPPAPI):
        # 模拟WXAPPAPI对象的exchange_code_for_session_key方法返回的session_info
        mock_session_info = {'openid': 'mock_openid'}
        MockWXAPPAPI.return_value.exchange_code_for_session_key.return_value = mock_session_info

        # 设置请求URL
        url = reverse('store_register')
        
        # 准备POST请求的数据
        data = {
            'code': 'mock_code',
            'name': 'mock_name',
            'location': 'mock_location',
            'phone': 'mock_phone',
            'avatar_url': 1
            # 根据需要设置其他字段
        }

        # 发送POST请求
        response = self.client.post(url, data, format='json')

        # 断言响应状态码为200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 断言响应数据中包含token
        self.assertIn('token', response.data)

    def test_valid_token(self):

        print("test7:使用有效 Token 发送 GET 请求**********")
       
        
        # 发送 POST 请求
        token = self.token
        # 设置请求头
        headers = {'HTTP_AUTHORIZATION': token}
        # 使用有效 Token 发送 GET 请求
        url = reverse('TestTokenView')
        response = self.client.get(url, **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, '成功获取信息')
        print('\n')

    






#         print('\n')

        # 发送 GET 请求，并传递筛选条件
# Create your tests here.
# class StudentTestCase(TestCase):
#     """
#     def setUp(self)：用来初始化环境，包括创建初始数据，或做一些其他准备工作
#     def test_xxx(self)：xxx可以是任何东西，以test_开头的方法，都会被django认为是需要测试的方法，跑测试时会被执行。
#         注：每个需要被测试的方法都是相互独立的
#     def tearDown(self)：跟setUp相对，用来清理测试环境和测试数据（在django中可以不关心这个）
#     """
#     def setUp(self):
#         # print('setUp')
#         self.user=User.objects.create(
#             username='stu1',
#             phone='111',
#             email='test1@qq.com',
#             password='333'
#         )
#         # print("userid:",self.user.id)
#         self.token=create_token({'user_id': self.user.id, 'username': self.user.username})
#         # 创建一个 Django 测试客户端
#         self.client = Client()

#     def test_user_model(self):
#         print('\n')
#         print('test1:测试用户创建')
#         self.assertEqual(self.user.username, 'stu1')
#         self.assertEqual(self.user.phone, '111')
#         self.assertEqual(self.user.email, 'test1@qq.com')
#         print('\n')

#     def test_login(self):
#         print('\n')
#         print("test2:测试token生成")
#         # 构造 POST 请求数据
#         data = {
#             'name': 'stu1',
#             'password': '333'
#         }
#         self.assertEqual(self.user.username, 'stu1')
#         self.assertEqual(self.user.password, '333')
#         # 发送 POST 请求
#         response = self.client.post(reverse('UserLogin'), data, format='json')
#         # 检查响应状态码是否为 200
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # 检查响应数据中是否包含预期的内容
#         self.assertIn('token', response.data)
#         print('\n')

#     def test_no_token(self):
#         print('\n')
#         print("test3:发送没有 Token 的 GET 请求")
        
#         # 发送没有 Token 的 GET 请求
#         response = self.client.get(reverse('TestTokenView'))
#         print("response data:",response.data)
#         # self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # self.assertEqual(response.data['code'], 1003)
#         # self.assertEqual(response.data['error'], 'token认证失败')
#          # 将响应数据转换为字典
#         response_data = json.loads(response.content)
        
#         # 检查返回的字典是否符合预期
#         self.assertEqual(response_data['code'], '1003')
#         self.assertEqual(response_data['error'], 'token认证失败')
#         print('\n')

#     def test_invalid_token(self):
#         print('\n')
#         print("test4:使用无效 Token 发送 GET 请求")
        
#         # 使用无效 Token 发送 GET 请求
#         invalid_token = 'invalid_token'
#         url = reverse('TestTokenView') + '?token=' + invalid_token
#         response = self.client.get(url)
#         response_data = json.loads(response.content)
        
#         # 检查返回的字典是否符合预期
#         self.assertEqual(response_data['code'], '1003')
#         self.assertEqual(response_data['error'], 'token认证失败')
#         print('\n')

#     def test_valid_token(self):

#         print('\n')
#         print("test5:使用有效 Token 发送 GET 请求")
#         data = {
#             'name': 'stu1',
#             'password': '333'
#         }
#         self.assertEqual(self.user.username, 'stu1')
#         self.assertEqual(self.user.password, '333')
#         # 发送 POST 请求
#         response = self.client.post(reverse('UserLogin'), data, format='json')
#         token = self.token
#         # 使用有效 Token 发送 GET 请求
#         url = reverse('TestTokenView') + '?token=' + token
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, '成功获取信息')
#         print('\n')

