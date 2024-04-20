from django.conf import settings

from weixin import WXAPPAPI
from weixin.oauth2 import OAuth2AuthExchangeError

from rest_framework.views import APIView
from rest_framework.response import Response
from tjeatwhatApp.models import usermodels

from tjeatwhatApp.utils.jwt_auth import create_token




class UserLogin(APIView):
    authentication_classes = []
    def post(self, request,*args,**kwargs):
        print("request.data: ",request.data)
        username = request.data.get('name')
        pwd = request.data.get('password')
        #过滤数据库中的数据，如果有对应的数据则返回第一个
        user_obj=usermodels.User.objects.filter(username=username,password=pwd).first()

        if not user_obj:
            return Response({'code':1000,'msg':'用户名或密码错误'})
        #如果找到就生成token
        token=create_token({'user_id': user_obj.id, 'username': user_obj.username})
        return Response({'code': 10001, 'token': token})
    
class WeixinLogin(APIView):
    authentication_classes = []
    def post(self, request,*args,**kwargs):
        print("request.data:",request.data)
        # 获取请求中的 code
        code = request.data.get('code')
        if code:
            # 使用 appid 和 app_secret 创建 WXAPPAPI 对象
            api = WXAPPAPI(appid=settings.WX_APP_ID, app_secret=settings.WX_APP_SECRET)
            try:
                # 使用 code 交换 session_key
                session_info = api.exchange_code_for_session_key(code=code)
            except OAuth2AuthExchangeError:
                # 如果发生 OAuth2AuthExchangeError 异常，将 session_info 设置为 None
                session_info = None
                
            if session_info:
                # 获取 openid
                openid = session_info.get('openid', None)
                if openid:
                    # 调用 create_or_update_user_info 函数创建或更新用户信息
                    user = usermodels.User.objects.filter(openid=openid).first()
                    if not user:
                        user = usermodels.User.objects.create(openid=openid)
                    # 生成 JWT token，并返回用户对象和 token
                    token = create_token({'user_id': user.id, 'username': user.username})
                    return Response({'code': 10001, 'token': token})
