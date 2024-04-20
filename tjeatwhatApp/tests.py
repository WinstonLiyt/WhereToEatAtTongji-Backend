from django.test import TestCase, Client 
from django.urls import reverse 
from django.core.files.uploadedfile import SimpleUploadedFile
from .views import * 
from .models import Restaurant,Dish,DishTag,User,DishEval 
import json
import os

class GXTestCase1(TestCase):
    def setUp(self): 
    # 创建一个测试用户 
        self.tag1=DishTag.objects.create(name='焦糖')
        self.tag2=DishTag.objects.create(name='快乐水')
        self.rest=Restaurant.objects.create(name='啦啦啦',location='B楼',description='太酷了',image='test_iamge.jpg',phone_number='456789')
        self.dish=Dish.objects.create(name='可乐',description='牛',image='test_iamge.jpg',price=5.2,restaurant=self.rest)
        self.dish.tags.set([self.tag1,self.tag2])
        self.Rest_id=0
        self.Dish_id=0
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
        self.assertEqual(response.status_code, 200)
        
    
    def test_create_restaurant(self):
        print()  
        print('test2:create_rest') 
        data = {'name': 'test_rest',
                'location':'安楼',
                'description': None,
                'image':'test_image.jpg',
                'phone_number':'123456'
                } 
        # 发送POST请求 
        response = self.client.post(reverse('create_restaurant'), json.dumps(data), content_type='application/json')
        response_data = json.loads(response.content) 
        print(response_data['time'])
        self.Rest_id=response_data['id']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Restaurant.objects.filter(image='test_image.jpg').exists())
        
        
    

    def test_delete_restaurant(self):
        print()  
        print('test3:delete_restaurant') 
        self.assertTrue(Restaurant.objects.filter(name='啦啦啦').exists()) 
        response = self.client.delete(reverse('delete_restaurant',kwargs={'id':self.rest.id}))
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
        response = self.client.post(reverse('create_dish',kwargs={'id':self.rest.id}), json.dumps(data), content_type='application/json')
        response_data = json.loads(response.content) 
        print(response_data['time'])
        self.Dish_id=response_data['id']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Dish.objects.filter(name='汉堡').exists()) 
    
    
    def test_delete_dish(self):
        print()  
        print('test5:delete_dish') 
        self.assertTrue(Dish.objects.filter(name='可乐').exists()) 
        response = self.client.delete(reverse('delete_dish',kwargs={'id':self.rest.id,'dish_id':self.dish.id}))
        response_data = json.loads(response.content) 
        print(response_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Dish.objects.filter(name='可乐').exists()) 



class GXTestCase2(TestCase):
    def setUp(self): 
    # 创建一个测试用户 
        self.tag1=DishTag.objects.create(name='焦糖')
        self.tag2=DishTag.objects.create(name='快乐水')
        self.rest=Restaurant.objects.create(name='啦啦啦',location='B楼',description='太酷了',image='test_iamge.jpg',phone_number='456789')
        self.dish=Dish.objects.create(name='可乐',description='牛',image='test_iamge.jpg',price=5.2,restaurant=self.rest)
        self.dish.tags.set([self.tag1,self.tag2])
        # 创建一个Django测试客户端 
        self.client = Client() 
    
        
    
    def test_update_restaurant(self):
        print()  
        print('test6:update_rest') 
        # 构造POST请求数据 
        data = {'name': 'KFC',
                'description': '疯狂星期四'
                } 
        # 发送POST请求 
        response = self.client.put(reverse('update_restaurant',kwargs={'id':self.rest.id}), json.dumps(data), content_type='application/json')
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
        response = self.client.put(reverse('update_dish',kwargs={'id':self.rest.id,'dish_id':self.dish.id}), json.dumps(data), content_type='application/json')
        response_data = json.loads(response.content) 
        print(response_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(DishTag.objects.filter(name='美味').exists()) 

