from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from .usermodels import UserSerializer
from .restaurantmodels import RestaurantSerializer


class Dish(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=32)#店名
    description=models.CharField(max_length=150,null=True)#餐品描述
    #tags = models.ManyToManyField('DishTag')#标签
    image = models.ImageField(upload_to='images', max_length=100, blank=True, null=True)  
    price=models.DecimalField(max_digits=5,decimal_places=2)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        # 删除旧图片
        if self.pk and self.image:
            old_dish = Dish.objects.get(pk=self.pk)
            if old_dish.image:
                old_dish.image.delete(False)  # 删除旧图片文件
        super().save(*args, **kwargs)



class DishEval(models.Model):
    id=models.AutoField(primary_key=True)
    score=models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])   #评分
    dish=models.ForeignKey("Dish", on_delete=models.CASCADE) #外键dish
    user=models.ForeignKey("User",on_delete=models.SET_NULL,null=True) #外键user
    comment=models.CharField(max_length=200)#餐品描述
    time=models.DateField() #评价时间
    reply=models.CharField(max_length=200,null=True)#店家回复
    reply_time=models.DateField(null=True)#回复时间



#序列化restaurant数据
class DishSerializer(serializers.ModelSerializer):
    #tags = DishTagSerializer(many=True, read_only=True)
    restaurant=RestaurantSerializer(read_only=True)
    class Meta:
        model = Dish
        fields = ['id', 'name',  'description', 'price','image','restaurant']

class DishEvalSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = DishEval
        fields = ['id', 'score','user', 'comment', 'time', 'reply']        



