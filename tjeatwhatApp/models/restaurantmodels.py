from django.db import models
from rest_framework import serializers


class RestTag(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=32,unique=True)#标签名

class RestImage(models.Model):
    id=models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images', max_length=100, blank=True, null=True)


class Restaurant(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=32)#店名
    location=models.CharField(max_length=32)#地址
    phone_number=models.CharField(max_length=11)#电话号码
    description=models.CharField(max_length=150,null=True)#店铺描述
    owner=models.ForeignKey('User',on_delete=models.CASCADE,default=None)
    images = models.ManyToManyField('RestImage', blank=True)
    tags=models.ManyToManyField('RestTag')

    def update_images(self, new_images):
        old_images = list(self.images.all())  # 获取当前餐厅的所有旧图片
         # 清空当前餐厅的所有图片联系
        self.images.clear()
        # 添加新的图片
        for image in new_images:
            rest_image, created = RestImage.objects.get_or_create(image=image)
            self.images.add(rest_image)
        
        # 删除不再被使用的旧图片对应的RestImage对象
        for old_image in old_images:
            if old_image not in self.images.all():
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
        fields = ['id', 'name', 'location', 'phone_number', 'description', 'images','tags']




    

