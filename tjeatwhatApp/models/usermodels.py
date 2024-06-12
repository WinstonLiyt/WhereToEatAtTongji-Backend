import hashlib
from rest_framework import serializers

from django.conf import settings
# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    id=models.AutoField(primary_key=True)
    USER_TYPE = ((1, '顾客'),
                 (2, '商家'),
                 (3,'管理员'),
                 (4,'客服'))

    TOKEN_TYPE = (
        (1, '绿牌'),
        (2,'蓝牌'),
        (3,'黄牌')
    )
    STATUS_TYPE = (
        (0, '禁用'),
        (1,'激活')
    )
    openid = models.CharField('微信openid', max_length=100, unique=True)
    nickname = models.CharField('微信昵称', max_length=100, blank=True, null=True)
    avatar_url = models.URLField('微信头像', blank=True, null=True)
    signature = models.CharField('个性签名', max_length=100, blank=True, null=True)
    type = models.IntegerField('用户类型', choices=USER_TYPE, default=1)
    credits = models.IntegerField('经验值', default=0)
    token = models.IntegerField('牌子', choices=TOKEN_TYPE, default=2)
    status=models.IntegerField('激活状态', choices=TOKEN_TYPE, default=1)
    
    def save(self, *args, **kwargs):
        # 在保存之前执行额外的操作
        if self.credits >= 1000:
            self.token=3
        if self.credits <1000:
            self.token=2
        super(User, self).save(*args, **kwargs)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'openid', 'nickname', 'avatar_url', 'type', 'credits','token']
