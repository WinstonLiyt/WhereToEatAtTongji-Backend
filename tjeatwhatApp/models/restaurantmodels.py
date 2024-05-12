from django.db import models
from rest_framework import serializers
import re



class RestTag(models.Model):
    TAG_TYPE = (
        (1, '面食'),
        (2,'甜点'),
        (3,'饮品'),
        (4,'早品'),
        (5,'水果'),
        (6,'烧烤'),
        (7,'西餐'),
        (8,'炒菜'),
    )
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=32,unique=True,choices=TAG_TYPE)#标签名

class RestImage(models.Model):
    id=models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images', max_length=100, blank=True, null=True,default='images/default_image.jpg')


class Restaurant(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=32)#店名
    location=models.CharField(max_length=32)#地址
    time=models.CharField(max_length=32,null=True)#营业时间
    phone_number=models.CharField(max_length=11)#电话号码
    description=models.CharField(max_length=150,null=True)#店铺描述
    owner=models.ForeignKey('User',on_delete=models.CASCADE,default=None)
    images = models.ManyToManyField('RestImage', blank=True)
    tags=models.ManyToManyField('RestTag')

    def update_images(self, new_images):
        # 获取当前餐厅的所有旧图片
        old_images = list(self.images.all())
        
        # 更新图片集合
        #从media开始
        # new_rest_images = [RestImage.objects.get_or_create(image=image)[0] for image in new_images]

        # 使用列表推导式处理图片路径，删除 "media" 前缀
        new_rest_images = [RestImage.objects.get_or_create(image=image.replace('/media/', ''))[0] for image in new_images]

        self.images.set(new_rest_images)

        # 删除不再被使用的旧图片对应的RestImage对象
        for old_image in old_images:
            # 检查旧图片是否还被其他餐厅使用
            if old_image.restaurant_set.count() == 0:
                old_image.delete()

  



class RestTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestTag
        fields = ['id', 'name']

class RestImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestImage
        fields = ['id', 'image']        



#序列化restaurant数据
class RestaurantSerializer(serializers.ModelSerializer):
    tags = RestTagSerializer(many=True, read_only=True)
    images = RestImageSerializer(many=True, read_only=True)
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'time','location', 'phone_number', 'description', 'images','tags']




    

