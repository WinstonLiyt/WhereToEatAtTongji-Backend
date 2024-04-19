from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from ..models.restaurantmodels import Restaurant


'''店铺的增删改部分'''


@csrf_exempt  #正式上线时去掉
def create_restaurant(request):
    if request.method == 'POST':
        # 获取请求体中的数据
        data = json.loads(request.body)
        # 解析请求体中的数据
        name = data.get('name', '')
        location = data.get('location', '')
        description = data.get('description', '')
        image = data.get('image', '')
        phone_number = data.get('phone_number', '')

        # 创建新的店铺记录
        new_restauant = Restaurant.objects.create(
            name=name,
            location=location,
            description=description,
            image=image,
            phone_number=phone_number,
        )
        
        # 构造返回的 JSON 数据
        response_data = {
            'id': new_restauant.id,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'message': 'Restaurant created successfully',
        }
        
        return JsonResponse(response_data,status=200)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)



@csrf_exempt 
def update_restaurant(request,id):
    try:
        rest = Restaurant.objects.get(pk=id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'error': 'Restaurant not found'}, status=404)

    if request.method == 'PUT':
        data = json.loads(request.body)
        #data.get如果键不存在，则返回rest.name，即默认使用当前店铺对象的名称作为值,这样就可以前端没传也可以不篡改数据
        rest.name = data.get('name', rest.name)
        rest.location = data.get('location', rest.location)
        rest.description = data.get('description', rest.description)
        rest.phone_number = data.get('phone_number', rest.phone_number)
        rest.image=data.get('image',rest.image)
        rest.save()
        return JsonResponse({'message': 'Shop updated successfully'},status=200)
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed'}, status=405)


@csrf_exempt 
def delete_restaurant(request,id):
    try:
        rest = Restaurant.objects.get(pk=id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'error': 'Restaurant not found'}, status=404)

    if request.method == 'DELETE':
        rest.delete()
        return JsonResponse({'message': 'Restaurant deleted successfully'})
    else:
        return JsonResponse({'error': 'Only DELETE requests are allowed'}, status=405)
    

'''店家回复评论'''







'''顾客查看全部店家'''

