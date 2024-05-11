# 导入django配置文件
from django.conf import settings
# 从drf中导入认证模块
from rest_framework.authentication import BaseAuthentication
# 从drf中导入认证异常模块
from rest_framework.exceptions import AuthenticationFailed
import jwt
from jwt import exceptions


class JwtQueryParamsAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 获取token并判断token的合法性
        #token = request.query_params.get('token')
        # 获取token并判断token的合法性
        # 打印请求头
        # print("header:",request.headers)
        token = request.headers.get('Token')

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

