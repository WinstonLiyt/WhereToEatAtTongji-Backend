from django.db import models

class Restaurant(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=32)#店名
    location=models.CharField(max_length=32)#地址
    phone_number=models.CharField(max_length=11)#电话号码
    description=models.CharField(max_length=150)#店铺描述
    image = models.ImageField(upload_to='images', max_length=100, blank=True, null=True)




    

