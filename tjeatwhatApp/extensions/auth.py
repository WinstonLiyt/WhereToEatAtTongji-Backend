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
        print("header:",request.headers)
        token = request.headers.get('Authorization')
        if not token:
            print("token不存在  ")
        #print("token=",token)
            #eturn None
        #print(token)
        # 1.切割
        # 2, 解密第二段/判断过期
        # 3，验证第三段合法性
        # 在drf里面对其进行了封装，会产生三种结果
        # 1.抛出异常，后续不再执行
        # 2.return一个元组(1,2),在视图中如果调用request.user，就是元组的第一个值，即payload；request.auth为第二个，即token
        # 3. None
        # 也就是说，只需要token跟salt，就能验证token是否正确，其详细操作可以查看源码，其实就是按照jwt，对其各步骤进行了封装

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

