# 导入django配置文件
from django.conf import settings
# 从drf中导入认证模块
from rest_framework.authentication import BaseAuthentication
# 从drf中导入认证异常模块
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import authentication_classes
import jwt
from jwt import exceptions

class EmptyParamsAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # print("header:",request.headers)
        token = request.headers.get('Token')
        # print("token:",token)
        if not token:
            print("token不存在  ")
            return ({'id':""},None)
            # raise AuthenticationFailed({'code': 1003, 'error': 'token未提供'})
        # 使用django配置中的SECRET_KEY作为盐
        salt = settings.SECRET_KEY

        try:
            payload = jwt.decode(token, salt, algorithms='HS256')
        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed({'code': 1003, 'error': 'token已失效'})
        except jwt.DecodeError:
            raise AuthenticationFailed({'code': 1003, 'error': 'token认证失败'})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({'code': 1003, 'error': '非法的token'})
        print("payload:",payload)
        return (payload, token)

class JwtQueryParamsAuthentication(BaseAuthentication):
    # def __init__(self):
    #     """
    #     初始化方法，设置是否进行严格的 token 检查
    #     """
    #     self.strict = strict
    def authenticate(self, request):
        # if not self.strict:
        #     # 如果不是严格模式，可以跳过 token 检查
        #     return None
       
        # 获取token并判断token的合法性
        # 打印请求头
        # print("header:",request.headers)
        token = request.headers.get('Token')
        # print("token:",token)
        if not token:
            print("token不存在  ")
            raise AuthenticationFailed({'code': 1003, 'error': 'token未提供'})
        # 使用django配置中的SECRET_KEY作为盐
        salt = settings.SECRET_KEY

        try:
            payload = jwt.decode(token, salt, algorithms='HS256')
        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed({'code': 1003, 'error': 'token已失效'})
        except jwt.DecodeError:
            raise AuthenticationFailed({'code': 1003, 'error': 'token认证失败'})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({'code': 1003, 'error': '非法的token'})
        
        return (payload, token)

