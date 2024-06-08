from django.conf import settings
from django.http import JsonResponse
from weixin import WXAPPAPI
from weixin.oauth2 import OAuth2AuthExchangeError
from tjeatwhatApp.extensions.auth import JwtQueryParamsAuthentication,JwtQueryParamsAuthentication2
from rest_framework.views import APIView
from rest_framework.response import Response
from tjeatwhatApp.models import usermodels,restaurantmodels
from rest_framework.decorators import api_view, authentication_classes
from tjeatwhatApp.utils.jwt_auth import create_token
from uuid import uuid4
import urllib.request
import os

##管理员禁用用户或激活用户
@api_view(['POST'])
@authentication_classes([JwtQueryParamsAuthentication])
def setUserStatus(request,*args,**kwargs):
    user_id = request.user.get('id')
    if not user_id:
        return Response({'msg': '没有id'}, status=403)
    user = usermodels.User.objects.get(id=user_id)
    if user.type!=3:
        return Response({'msg':'非管理员，没有权限'},status=401)
    setUser_id=request.data.get('userid')
    setUser_status=request.data.get('status')
    if not setUser_id:
        return Response({'msg': '没有id'}, status=403)
    setUser=usermodels.User.objects.get(id=setUser_id)
    if not setUser:
        return Response({'msg':'没有该用户'},status=404)
    setUser.status=setUser_status
    setUser.save()
    return Response({'msg':'success'},status=200)

##管理员设置用户信息
@api_view(['POST'])
@authentication_classes([JwtQueryParamsAuthentication])
def setUserinfoByManager(request,*args,**kwargs):
    user_id = request.user.get('id')
    if not user_id:
        return Response({'msg': '没有id'}, status=403)
    user = usermodels.User.objects.get(id=user_id)
    if user.type!=3:
        return Response({'msg':'非管理员，没有权限'},status=401)
    setUser_id=request.data.get('userid')
    if not setUser_id:
        return Response({'msg': '没有id'}, status=403)
    setUser=usermodels.User.objects.get(id=setUser_id)
    if not setUser:
        return Response({'msg':'没有该用户'},status=404)
    
    new_credits=int(request.data.get('credits'))
    setUser.credits=new_credits
    setUser.save()
    return Response({'msg': 'success'}, status=200)

##管理员获取用户列表
@api_view(['GET'])
@authentication_classes([JwtQueryParamsAuthentication])
def get_user_list(request,*args,**kwargs):
    user_id = request.user.get('id')
    if not user_id:
        return Response({'msg': '没有id'}, status=403)
    user = usermodels.User.objects.get(id=user_id)
    if user.type!=3:
        return Response({'msg':'非管理员，没有权限'},status=401)
    # users=usermodels.User.objects.all().values('id','nickname','type','status')
    users = usermodels.User.objects.filter(type__in=[1, 2]).values('id', 'nickname', 'type', 'status')

    if users:
        return Response({'data':users},status=200)
    else:
        return Response({'message':'no user'},status=404)

##管理员获取指定用户信息
@api_view(['GET'])
@authentication_classes([JwtQueryParamsAuthentication])
def get_user_info_by_manager(request,*args,**kwargs):
    user_id = request.user.get('id')
    if not user_id:
        return Response({'msg': '没有id'}, status=403)
    user = usermodels.User.objects.get(id=user_id)
    if user.type!=3:
        return Response({'msg':'非管理员，没有权限'},status=401)
    getUser_id = request.GET.get('userid')
    if not getUser_id:
        return Response({'msg': '没有id'}, status=403)
    getUser=usermodels.User.objects.get(id=getUser_id)
    if not getUser:
        return Response({'msg':'没有该用户'},status=404)
    userInfo={'name':getUser.nickname,
    'avatar_url':getUser.avatar_url,
    'signature':getUser.signature,
    'credits':getUser.credits,
    'status':getUser.status}
    return Response(userInfo, status=200)



@api_view(['GET'])
@authentication_classes([JwtQueryParamsAuthentication])
def get_user_id(request,*args,**kwargs):
    user_id = request.user.get('id')
    return Response({'id':user_id},status=200)

##获取用户基本信息
@api_view(['GET'])
@authentication_classes([JwtQueryParamsAuthentication2])
def get_user_info(request,*args,**kwargs):
    user_id = request.user.get('id')
    if user_id:
        user = usermodels.User.objects.get(id=user_id)
        name=user.nickname
        signature=user.signature
        avatar_url=user.avatar_url
        credit=user.credits
        tokencard=user.token

        return Response({'name':name,'signature': signature,'avatar_url':avatar_url,'credits':credit,'tokencard':tokencard},status=200)
    else:
        return Response({'error': '获取用户信息失败'}, status=405)


##上传头像
@api_view(['POST'])
def upload_avatar(request,*args,**kwargs):
    if request.FILES.get('file'):
        file= request.FILES['file']
        # 处理上传的文件，保存到服务器上
        _, ext = os.path.splitext(file.name)
        new_name = f"{uuid4().hex}{ext}"
        # print("newname:",new_name)
        where = '%s/avatar/%s' % (settings.MEDIA_ROOT, new_name)
        # 分块保存image
        content = file.chunks()
        with open(where, 'wb') as f:
            for i in content:
                f.write(i)
        
        return Response({'newname':new_name,'message': 'File uploaded successfully'},status=200)
    else:
        return Response({'error': '只能上传图片文件'}, status=405)


##`用户登录`
@api_view(['POST'])
def login(request,*args,**kwargs):
    code = request.data.get('code')
    if code:
        # 使用 appid 和 app_secret 创建 WXAPPAPI 对象
        api = WXAPPAPI(appid=settings.WX_APP_ID, app_secret=settings.WX_APP_SECRET)
        try:
            # print("api",api)
            # 使用 code 交换 session_key
            session_info = api.exchange_code_for_session_key(code=code)
        except OAuth2AuthExchangeError:
            # 如果发生 OAuth2AuthExchangeError 异常，将 session_info 设置为 None
            session_info = None
            return Response({ 'error': 'code传递成功但获取 openid 失败'}, status=504)

        if session_info:
            # 获取 openid
            openid = session_info.get('openid', None)
            if openid:
                # 调用 create_or_update_user_info 函数创建或更新用户信息
                user = usermodels.User.objects.filter(openid=openid).first()
                if not user:
                    return Response({'error': '用户不存在'},status=404)
                    
                # 生成 JWT token，并返回用户对象和 token
                token = create_token({'id': user.id,'openid': user.openid})
                return Response({'token': token,'role':user.type},status=200)
            
    # 如果没有成功获取 openid，返回相应的错误响应
    return Response({ 'error': '获取 openid 失败'}, status=501)


##`学生身份注册`

@api_view(['POST'])
def student_register(request,*args,**kwargs):
    code = request.data.get('code')
    name = request.data.get('name')
    avatar_url = request.data.get('avatar_url')
    
    if not avatar_url:
        avatar_url="default.jpg"

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
                return Response({ 'token': token},status=200)
    
    # 如果没有成功注册用户，返回错误响应
    return Response({'error': '注册学生身份失败'}, status=400)

##`商家身份注册

@api_view(['POST'])
def store_register(request,*args,**kwargs):
    code = request.data.get('code')
    name = request.data.get('name')
    location = request.data.get('location')
    phone = request.data.get('phone')
    avatar_url = request.data.get('avatar_url')

    rest_image=restaurantmodels.RestImage.objects.create(image="images/default_image.jpg")
    
    
    if not avatar_url:
        avatar_url="default.jpg"
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
                    avatar_url=avatar_url,
                    # 根据需要设置其他字段
                )
                restaurant = restaurantmodels.Restaurant.objects.create(
                    name=name,
                    location=location,
                    phone_number=phone,
                    owner=user
                )
                restaurant.images.set([rest_image])
                restaurant.save()

                # 生成 JWT token，并返回用户对象和 token
                token = create_token({'id': user.id,'openid': user.openid})
                return Response({ 'token': token}, status=200)
    
    # 如果没有成功注册用户，返回错误响应
    return Response({'error': '注册商家身份失败'}, status=400)

##设置个人信息
@api_view(['POST'])
@authentication_classes([JwtQueryParamsAuthentication])
def set_user_info(request,*args,**kwargs):
    nickname = request.data.get('nickname')
    signature = request.data.get('signature')
    avatar_url = request.data.get('avatar_url')
    user_id = request.user.get('id')
    if nickname and avatar_url :
        user = usermodels.User.objects.get(id=user_id)
        # if signature:
        user.signature=signature
        user.nickname = nickname
        user.avatar_url = avatar_url
        user.save()
        return Response({'msg': '成功修改信息'}, status=200)
    return Response({'error': '关键字段缺失'}, status=400)

##`设置签名`
@api_view(['POST'])
@authentication_classes([JwtQueryParamsAuthentication])
def set_signature(request,*args,**kwargs):
    signature = request.data.get('signature')
    user_id = request.user.get('id')
    
    if signature:
        user = usermodels.User.objects.get(id=user_id)
        print("user_id:",user.id)
        user.signature=signature
        print("user_signature:",user.signature)
        user.save()
        print("user_signature:",user.signature)
        return Response({'msg': '成功修改签名'}, status=200)

    return Response({'error': '签名不能为空'}, status=400)

##`设置用户名`
@api_view(['POST'])
@authentication_classes([JwtQueryParamsAuthentication])
def set_name(request,*args,**kwargs):
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