import hashlib

from django.conf import settings
# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):

    USER_TYPE = ((1, '顾客'),
                 (2, '商家'),
                 (3,'管理员'),
                 (4,'客服'))

    TOKEN_TYPE = (
        (1, '绿牌'),
        (2,'蓝牌'),
        (3,'黄牌')
    )

    username = models.CharField('用户名', max_length=150, unique=True)
    phone = models.CharField('电话', max_length=20, blank=True, null=True)
    email = models.EmailField('邮箱', unique=True)
    password = models.CharField('密码', max_length=128)
    # 微信账号相关信息
    openid = models.CharField('微信openid', max_length=100, unique=True, blank=True, null=True)
    unionid = models.CharField('微信unionid', max_length=100, unique=True, blank=True, null=True)
    wx_nickname = models.CharField('微信昵称', max_length=100, blank=True, null=True)
    wx_avatar_url = models.URLField('微信头像', blank=True, null=True)

    type = models.IntegerField('用户类型', choices=USER_TYPE, default=1)
    credits = models.IntegerField('经验值', default=0)
    token = models.IntegerField('牌子', choices=TOKEN_TYPE, default=1)
    # 用自定义的用户需要重写此方法
    def create_username_password(self):
        if not self.username and not self.password and self.openid:
            key = settings.SECRET_KEY
            self.username = hashlib.pbkdf2_hmac(
                "sha256", getattr(self, 'openid').encode(encoding='utf-8'), key.encode(encoding='utf-8'), 10).hex()
            self.password = hashlib.pbkdf2_hmac(
                "sha256", self.username.encode(), getattr(self, 'openid').encode(encoding='utf-8'), 10).hex()

    def save(self, *args, **kwargs):
        self.create_username_password()
        super().save(*args, **kwargs)


    


# class User(AbstractUser):

#     USER_TYPE = ((1, '顾客'),
#                  (2, '商家'),
#                  (3,'管理员'),
#                  (4,'客服'))

#     TOKEN_TYPE = (
#         (1, '绿牌'),
#         (2,'蓝牌'),
#         (3,'黄牌')
#     )
    
    
#     # 微信账号相关信息
#     openid = models.CharField('微信openid', max_length=100, unique=True, blank=True, null=True)
#     unionid = models.CharField('微信unionid', max_length=100, unique=True, blank=True, null=True)
#     wx_nickname = models.CharField('微信昵称', max_length=100, blank=True, null=True)
#     wx_avatar_url = models.URLField('微信头像', blank=True, null=True)

#     type = models.IntegerField('用户类型', choices=USER_TYPE, default=1)
#     credits = models.IntegerField('经验值', default=0)
#     token = models.IntegerField('牌子', choices=TOKEN_TYPE, default=1)
#     # 用自定义的用户需要重写此方法
#     def create_username_password(self):
#         if not self.username and not self.password and self.openid:
#             key = settings.SECRET_KEY
#             self.username = hashlib.pbkdf2_hmac(
#                 "sha256", getattr(self, 'openid').encode(encoding='utf-8'), key.encode(encoding='utf-8'), 10).hex()
#             self.password = hashlib.pbkdf2_hmac(
#                 "sha256", self.username.encode(), getattr(self, 'openid').encode(encoding='utf-8'), 10).hex()

#     def save(self, *args, **kwargs):
#         self.create_username_password()
#         super().save(*args, **kwargs)


#     class Meta(AbstractUser.Meta):
#         swappable = 'AUTH_USER_MODEL'
