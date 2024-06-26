from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from rest_framework.decorators import api_view, authentication_classes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from ..models.restaurantmodels import Restaurant,RestaurantSerializer,RestImage,RestTag
from ..models.dishmodels import Dish,DishEval
from ..models.usermodels import User,UserSerializer
from tjeatwhatApp.extensions.auth import JwtQueryParamsAuthentication
from rest_framework.decorators import  authentication_classes
from tjeatwhatApp.extensions.auth import JwtQueryParamsAuthentication,EmptyParamsAuthentication
'''店铺的增删改部分'''


# # @authentication_classes([JwtQueryParamsAuthentication])
# @csrf_exempt
# def create_restaurant(request,user_id):
#     try:
#         user = User.objects.get(pk=user_id)
#     except User.DoesNotExist:
#         return JsonResponse({'error': 'User not found'}, status=404)
#     if request.method == 'POST':
#         # 获取请求体中的数据
#         data = json.loads(request.body)
#         # 解析请求体中的数据
#         name = data.get('name', '')
#         time=data.get('time','')
#         location = data.get('location', '')
#         description = data.get('description', '')
       
#         phone_number = data.get('phone_number', '')
#         if 'tags' in data and isinstance(data['tags'], list):
#             # 如果 JSON 数据中包含 'tags' 键且其值是一个数组
#             tag_names = data['tags']
#             tags = []
#             # 检查标签是否已存在，不存在则创建新标签
#             for tag_name in tag_names:
#                 tag, created = RestTag.objects.get_or_create(name=tag_name)
#                 tags.append(tag)
#         else:
#             return JsonResponse({'error': 'Invalid JSON data format'}, status=400)




#         #多张图片
#         images = data['images']
#         rest_images=[]
#         for image in images:
#                 rest_image, created = RestImage.objects.get_or_create(image=image)
#                 rest_images.append(rest_image)
        

#         # 创建新的店铺记录
#         new_restauant = Restaurant.objects.create(
#             name=name,
#             location=location,
#             time=time,
#             description=description,
#             phone_number=phone_number,
#             owner=user
#         )
#         new_restauant.images.set(rest_images)
#         new_restauant.tags.set(tags)
        
#         # 构造返回的 JSON 数据
#         response_data = {
#             'id': new_restauant.id,
#             'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#             'message': 'Restaurant created successfully',
#         }
        
#         return JsonResponse(response_data,status=200)
#     else:
#         return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)





#店家    
@api_view(['PUT'])
@authentication_classes([JwtQueryParamsAuthentication])
def update_restaurant(request):
    if request.method == 'PUT':
        user=User.objects.get(pk=request.user.get('id'))
        rest = Restaurant.objects.get(owner=user)
        data = json.loads(request.body)
        #data.get如果键不存在，则返回rest.name，即默认使用当前店铺对象的名称作为值,这样就可以前端没传也可以不篡改数据
        rest.name = data.get('name', rest.name)
        rest.time=data.get('time',rest.time)
        rest.location = data.get('location', rest.location)
        rest.description = data.get('description', rest.description)
        rest.phone_number = data.get('phone_number', rest.phone_number)
        #rest.image=data.get('image',rest.image)
        images=data['images']
       
        if not any(item is None for item in images):
            rest.update_images(images)
        if 'tags' in data:
            tag_names = data['tags']
            tags = []
            for tag_name in tag_names:
                tag, created = RestTag.objects.get_or_create(name=tag_name)
                tags.append(tag)
            rest.tags.set(tags)  # 设置菜品的标签关联
        # 如果标签数据为空，保留原有的标签关联
        elif 'tags' not in data and rest.tags.exists():
            pass


        rest.save()
        return JsonResponse({'message': 'Restaurant updated successfully'},status=200)
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed'}, status=405)






# @api_view(['DELETE'])
# @authentication_classes([JwtQueryParamsAuthentication])
# def delete_restaurant(request):
#     try:
#         rest = Restaurant.objects.get(pk=rest_id)
#     except Restaurant.DoesNotExist:
#         return JsonResponse({'error': 'Restaurant not found'}, status=404)

#     if request.method == 'DELETE':
#         rest.delete()
#         return JsonResponse({'message': 'Restaurant deleted successfully'},status=200)
#     else:
#         return JsonResponse({'error': 'Only DELETE requests are allowed'}, status=405)
    

'''店家回复评论'''

@api_view(['POST'])
@authentication_classes([JwtQueryParamsAuthentication])
def reply(request,eval_id):
    try:
        eval = DishEval.objects.get(pk=eval_id)
    except DishEval.DoesNotExist:
        return JsonResponse({'error': 'Dish evaluation not found'}, status=404)
    
    if request.method == 'POST':
     
        data = json.loads(request.body)
     
        reply = data.get('reply', '')
        
        # 创建新的回复
        eval.reply=reply
        eval.reply_time=datetime.now()

        eval.save()
        print(eval.reply_time)
        return JsonResponse({'message': 'Reply successfully','reply_time':eval.reply_time},status=200)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)



'''顾客查看全部店家'''

#所有人
@api_view(['GET'])
def get_all_rest(request):
    if request.method == 'GET':
         restaurants = Restaurant.objects.all()
         response = RestaurantSerializer(restaurants, many=True)
         return JsonResponse(response.data,safe=False,status=200)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)
    
#所有人
@api_view(['GET'])

def get_rest(request,rest_id):
    if request.method == 'GET':
         try:
            rest = Restaurant.objects.get(pk=rest_id)
         except Restaurant.DoesNotExist:
            return JsonResponse({'error': 'Restaurant not found'}, status=404)
        #  images=[RestImage.objects.get(pk=image.id) for image in rest.images]
        
         response_data=RestaurantSerializer(rest)

         return JsonResponse(response_data.data,status=200)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)
    

#店家    
@api_view(['GET'])
@authentication_classes([JwtQueryParamsAuthentication])
def get_self_rest(request):
    if request.method == 'GET':
         user=User.objects.get(pk=request.user.get('id'))
         try:
            rest = Restaurant.objects.get(owner=user)
         except Restaurant.DoesNotExist:
            return JsonResponse({'error': 'Restaurant not found'}, status=404)
        #  images=[RestImage.objects.get(pk=image.id) for image in rest.images]
        
         response_data=RestaurantSerializer(rest)
         

         return JsonResponse(response_data.data,status=200)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)


@api_view(['GET'])
@authentication_classes([JwtQueryParamsAuthentication])
def get_rest_id(request):
    if request.method == 'GET':
        user=User.objects.get(pk=request.user.get('id'))
        rest = Restaurant.objects.get(owner=user)

        

        return JsonResponse({'id':rest.id},status=200)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)       