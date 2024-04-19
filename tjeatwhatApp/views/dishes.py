from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from ..models.restaurantmodels import Tag,Dish,Restaurant

'''菜品的增删改'''

@csrf_exempt  #正式上线时去掉
def create_dish(request,id):
    if request.method == 'POST':
        # 获取请求体中的数据
        data = json.loads(request.body)
        # 解析请求体中的数据
        if 'tags' in data and isinstance(data['tags'], list):
            # 如果 JSON 数据中包含 'array_data' 键且其值是一个数组
            tags = data['tags']
        else:
            return JsonResponse({'error': 'Invalid JSON data format'}, status=400)
       
        name = data.get('name', '')
        rest=Restaurant.objects.get(pk=id)
        description = data.get('description', '')
        image = data.get('image', '')
        price = float(data.get('phone_number', 0))#转成浮点数

        # 创建新的店铺记录
        new_dish = Dish.objects.create(
            name=name,
            tags=tags,
            description=description,
            image=image,
            price=price,
            restaurant=rest,
        )


        # 构造返回的 JSON 数据
        response_data = {
            'id': new_dish.id,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'message': 'Restaurant created successfully',
        }
        
        return JsonResponse(response_data,status=200)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)



@csrf_exempt 
def update_dish(request,id,dish_id):
    try:
        rest = Restaurant.objects.get(pk=id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'error': 'Restaurant not found'}, status=404)
    
    try:
        dish = Dish.objects.get(pk=dish_id)
    except Dish.DoesNotExist:
        return JsonResponse({'error': 'Dish not found'}, status=404)

    if request.method == 'PUT':
        data = json.loads(request.body)
        dish.name = dish.get('name', dish.name)
        dish.tags = dish.get('tags', dish.tags)
        dish.description = data.get('description', dish.description)
        dish.price = float(data.get('price', dish.phone_number))
        dish.image=data.get('image',dish.image)
        dish.save()
        return JsonResponse({'message': 'Dish updated successfully'},status=200)
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed'}, status=405)


@csrf_exempt 
def delete_dish(request,id,dish_id):
    try:
        rest = Restaurant.objects.get(pk=id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'error': 'Restaurant not found'}, status=404)
    
    try:
        dish = Dish.objects.get(pk=dish_id)
    except Dish.DoesNotExist:
        return JsonResponse({'error': 'Dish not found'}, status=404)

    if request.method == 'DELETE':
        dish.delete()
        return JsonResponse({'message': 'Dish deleted successfully'})
    else:
        return JsonResponse({'error': 'Only DELETE requests are allowed'}, status=405)
    


'''顾客评论/点赞/删除评论菜品'''






    
'''顾客查看所有菜品'''   





'''顾客查看菜品的评价'''