from django.conf import settings

from weixin import WXAPPAPI
from weixin.oauth2 import OAuth2AuthExchangeError
from tjeatwhatApp.extensions.auth import JwtQueryParamsAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from tjeatwhatApp.models import usermodels,restaurantmodels
from rest_framework.decorators import api_view, authentication_classes
from tjeatwhatApp.utils.jwt_auth import create_token


##`用户登录`
@api_view(['POST'])
def login(request,*args,**kwargs):
    print("request.data:",request.data)
    # 获取请求中的 code
    code = request.data.get('code')
    print("code:",code)
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
            print("session_info:",session_info)
            # 获取 openid
            openid = session_info.get('openid', None)
            if openid:
                # 调用 create_or_update_user_info 函数创建或更新用户信息
                user = usermodels.User.objects.filter(openid=openid).first()
                print("user:",user)
                if not user:
                    return Response({'msg': '用户不存在'},status=404)
                    
                # 生成 JWT token，并返回用户对象和 token
                token = create_token({'id': user.id,'openid': user.openid})
                return Response({'token': token,'role':user.type},status=200)
            
    # 如果没有成功获取 openid，返回相应的错误响应
    return Response({ 'msg': '获取 openid 失败'}, status=500)


##`学生身份注册`

@api_view(['POST'])
def student_register(request,*args,**kwargs):
    print("request.data:",request.data)
    code = request.data.get('code')
    name = request.data.get('name')
    avatar_url = request.data.get('avatar_url')
    #这里记得加上头像处理*************

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
                user = usermodels.User.objects.create(
                    openid=openid,
                    nickname=name,
                    type=1,
                    token=2,
                    avatar_url=avatar_url
                    # 根据需要设置其他字段
                )
                # 生成 JWT token，并返回用户对象和 token
                token = create_token({'id': user.id,'openid': user.openid})
                return Response({'code': 200, 'token': token})
    
    # 如果没有成功注册用户，返回错误响应
    return Response({'error': 'Failed to register user'}, status=400)

##`商家身份注册

@api_view(['POST'])
def store_register(request,*args,**kwargs):
    print("request.data:",request.data)
    code = request.data.get('code')
    name = request.data.get('name')
    location = request.data.get('location')
    phone = request.data.get('phone')
    avatar_url = request.data.get('avatar_url')
    #这里记得加上头像处理*************

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
                user = usermodels.User.objects.create(
                    openid=openid,
                    nickname=name,
                    type=2,
                    avatar_url=avatar_url
                    # 根据需要设置其他字段
                )
                restaurant = restaurantmodels.Restaurant.objects.create(
                    name=name,
                    location=location,
                    phone_number=phone,
                    image=avatar_url
                )
                # 生成 JWT token，并返回用户对象和 token
                token = create_token({'id': user.id,'openid': user.openid})
                return Response({ 'token': token}, status=200)
    
    # 如果没有成功注册用户，返回错误响应
    return Response({'error': 'Failed to register user'}, status=400)

##`设置用户名`
@api_view(['POST'])
@authentication_classes([JwtQueryParamsAuthentication])
def set_name(request,*args,**kwargs):
    print("request.data:",request.data)
    nickname = request.data.get('nickname')
    user_id = request.user.get('id')

    if nickname:
        user = usermodels.User.objects.get(id=user_id)
        print("user_openid:",user.openid)
        user.nickname = nickname
        print("user_nickname:",user.nickname)
        user.save()
        print("user_nickname:",user.nickname)
        return Response({'msg': '成功修改用户名'}, status=200)

    return Response({'error': '用户名不能为空'}, status=400)

##`设置头像`
@api_view(['POST'])
@authentication_classes([JwtQueryParamsAuthentication])
def set_avatar(request,*args,**kwargs):
    print("request.data:",request.data)
    avatar_url = request.data.get('avatar_url')
    user_id = request.user.get('id')

    if avatar_url:
        user = usermodels.User.objects.get(id=user_id)
        print("user_openid:",user.openid)
        user.avatar_url = avatar_url
        #print("user_nickname:",user.nickname)
        user.save()
        #print("user_nickname:",user.nickname)
        return Response({'msg': '成功修改头像'}, status=200)

    return Response({'error': '头像不能为空'}, status=400)


##`测试token`
@api_view(['GET'])
@authentication_classes([JwtQueryParamsAuthentication])
def test_token_view(request):
    print("request.user:",request.user)
    print("request.auth:",request.auth)
    return Response('成功获取信息')



# class TestTokenView(APIView):
#     authentication_classes = [JwtQueryParamsAuthentication]
#     def get(self, request, *args, **kwargs):
        
#         # 1.切割
#         # 2, 解密第二段/判断过期
#         # 3，验证第三段合法性
#         print("request.data:",request.data)
#         print("request.user:",request.user)
#         print("request.auth:",request.auth)
#         return Response('成功获取信息')
# class UserLogin(APIView):
#     authentication_classes = []
#     def post(self, request,*args,**kwargs):
#         print("request.data: ",request.data)
#         username = request.data.get('name')
#         pwd = request.data.get('password')
#         #过滤数据库中的数据，如果有对应的数据则返回第一个
#         user_obj=usermodels.User.objects.filter(username=username,password=pwd).first()

#         if not user_obj:
#             return Response({'code':1000,'msg':'用户名或密码错误'})
#         #如果找到就生成token
#         token=create_token({'user_id': user_obj.id, 'username': user_obj.username})
        
#         return Response({'code': 10001, 'token': token})


