# 导入django配置文件
from django.conf import settings
# 从drf中导入认证模块
from rest_framework.authentication import BaseAuthentication
# 从drf中导入认证异常模块
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import authentication_classes
from tjeatwhatApp.models import usermodels
import jwt
from jwt import exceptions

from rest_framework.exceptions import APIException

class CustomAuthenticationFailed(APIException):
    status_code = 403
    default_detail = '用户被禁用'
    default_code = 'user_disabled'

class TokenAuthenticationFailed(APIException):
    status_code = 401
    default_detail = 'token验证失败'
    default_code = 'user_disabled'


class EmptyParamsAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Token')
        if not token:
            print("token不存在  ")
            return ({'id': None},None)
        # 使用django配置中的SECRET_KEY作为盐
        salt = settings.SECRET_KEY

        try:
            payload = jwt.decode(token, salt, algorithms='HS256')
        except exceptions.ExpiredSignatureError:
            raise TokenAuthenticationFailed({'code': 1003, 'error': 'token已失效'})
        except jwt.DecodeError:
            raise TokenAuthenticationFailed({'code': 1003, 'error': 'token认证失败'})
        except jwt.InvalidTokenError:
            raise TokenAuthenticationFailed({'code': 1003, 'error': '非法的token'})
        # print("payload:",payload)
        return (payload, token)

class JwtQueryParamsAuthentication(BaseAuthentication):
    def authenticate(self, request):
        
        token = request.headers.get('Token')
        print("token:",token)
        if not token:
            print("token不存在  ")
            raise TokenAuthenticationFailed({'code': 1003, 'error': 'token未提供'})
        # 使用django配置中的SECRET_KEY作为盐
        salt = settings.SECRET_KEY

        try:
            payload = jwt.decode(token, salt, algorithms='HS256')
            user_id=payload.get('id')
            user = usermodels.User.objects.get(id=user_id)
            if user.status==0:
                raise CustomAuthenticationFailed({'error': '用户被禁用'})
        except exceptions.ExpiredSignatureError:
            raise TokenAuthenticationFailed({'code': 1003, 'error': 'token已失效'})
        except jwt.DecodeError:
            raise TokenAuthenticationFailed({'code': 1003, 'error': 'token认证失败'})
        except jwt.InvalidTokenError:
            raise TokenAuthenticationFailed({'code': 1003, 'error': '非法的token'})
        
        return (payload, token)

class JwtQueryParamsAuthentication2(BaseAuthentication):
    def authenticate(self, request):
        
        token = request.headers.get('Token')

        if not token:
            print("token不存在  ")
            raise TokenAuthenticationFailed({'code': 1003, 'error': 'token未提供'})
        # 使用django配置中的SECRET_KEY作为盐
        salt = settings.SECRET_KEY

        try:
            payload = jwt.decode(token, salt, algorithms='HS256')
            user_id=payload.get('id')
            user = usermodels.User.objects.get(id=user_id)
            
        except exceptions.ExpiredSignatureError:
            raise TokenAuthenticationFailed({'code': 1003, 'error': 'token已失效'})
        except jwt.DecodeError:
            raise TokenAuthenticationFailed({'code': 1003, 'error': 'token认证失败'})
        except jwt.InvalidTokenError:
            raise TokenAuthenticationFailed({'code': 1003, 'error': '非法的token'})
        
        return (payload, token)

