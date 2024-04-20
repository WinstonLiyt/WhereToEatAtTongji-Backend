from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField


class DishTag(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=32,unique=True)#标签名


class Dish(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=32)#店名
    description=models.CharField(max_length=150,null=True)#餐品描述
    tags = models.ManyToManyField('DishTag')#标签
    image = models.ImageField(upload_to='images', max_length=100, blank=True, null=True)  
    price=models.DecimalField(max_digits=5,decimal_places=2)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)



class DishEval(models.Model):
    id=models.AutoField(primary_key=True)
    score=models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])   #评分
    dish=models.ForeignKey("Dish", on_delete=models.CASCADE) #外键dish
    user=models.ForeignKey("User",on_delete=models.SET_NULL,null=True) #外键user
    comment=models.CharField(max_length=200)#餐品描述
    time=models.DateTimeField() #评价时间
    reply=models.CharField(max_length=200)#店家回复

