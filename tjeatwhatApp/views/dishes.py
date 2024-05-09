from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from ..models.restaurantmodels import Restaurant,RestaurantSerializer
from ..models.dishmodels import  Dish,DishTag,DishSerializer,DishEval,DishEvalSerializer
from django.db.models import Avg
from ..models.usermodels import User
import jieba 
from ..apps import TjeatwhatappConfig
from rest_framework.response import Response


'''菜品的增删改'''

@csrf_exempt  #正式上线时去掉
def create_dish(request,rest_id):
    try:
        rest = Restaurant.objects.get(pk=rest_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'error': 'Restanuant not found'}, status=404)
    
    if request.method == 'POST':
        # 获取请求体中的数据
        data = json.loads(request.body)
        if 'tags' in data and isinstance(data['tags'], list):
            # 如果 JSON 数据中包含 'tags' 键且其值是一个数组
            tag_names = data['tags']
            tags = []
            # 检查标签是否已存在，不存在则创建新标签
            for tag_name in tag_names:
                tag, created = DishTag.objects.get_or_create(name=tag_name)
                tags.append(tag)
        else:
            return JsonResponse({'error': 'Invalid JSON data format'}, status=400)
       
        name = data.get('name', '')
        description = data.get('description', '')
        image = data.get('image', '')
        price = float(data.get('price', 0))#转成浮点数

        # 创建新的店铺记录
        new_dish = Dish.objects.create(
            name=name,
            description=description,
            image=image,
            price=price,
            restaurant=rest,
        )

        new_dish.tags.set(tags)


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
def update_dish(request,dish_id):
    try:
        dish = Dish.objects.get(pk=dish_id)
    except Dish.DoesNotExist:
        return JsonResponse({'error': 'Dish not found'}, status=404)

    if request.method == 'PUT':
        data = json.loads(request.body)
     
        if 'tags' in data:
            tag_names = data['tags']
            tags = []
            for tag_name in tag_names:
                tag, created = DishTag.objects.get_or_create(name=tag_name)
                tags.append(tag)
            dish.tags.set(tags)  # 设置菜品的标签关联
        # 如果标签数据为空，保留原有的标签关联
        elif 'tags' not in data and dish.tags.exists():
            pass

        dish.name = data.get('name', dish.name)
        dish.description = data.get('description', dish.description)
        dish.price = float(data.get('price', dish.price))
        dish.image=data.get('image',dish.image)
        dish.save()
        return JsonResponse({'message': 'Dish updated successfully'},status=200)
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed'}, status=405)




@csrf_exempt 
def delete_dish(request,dish_id):
    
    try:
        dish = Dish.objects.get(pk=dish_id)
    except Dish.DoesNotExist:
        return JsonResponse({'error': 'Dish not found'}, status=404)

    if request.method == 'DELETE':
        dish.delete()
        return JsonResponse({'message': 'Dish deleted successfully'},status=200)
    else:
        return JsonResponse({'error': 'Only DELETE requests are allowed'}, status=405)
    
'''获取一家店所有菜品'''

@csrf_exempt  #正式上线时去掉
def get_all_dish(request,rest_id):
    try:
        rest = Restaurant.objects.get(pk=rest_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'error': 'Restanuant not found'}, status=404)
    
    if request.method == 'GET':
         dishes = Dish.objects.filter(restaurant=rest)
         response = DishSerializer(dishes, many=True)
         return JsonResponse(response.data,safe=False,status=200)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)



@csrf_exempt  #正式上线时去掉
def get_dish(request,dish_id):
    if request.method == 'GET':
         try:
            dish = Dish.objects.get(pk=dish_id)
         except Dish.DoesNotExist:
            return JsonResponse({'error': 'Dish not found'}, status=404)
         response_data={
             'id':dish.id,
             'name':dish.name,
             'description':dish.description,
             'tags':dish.tags,
             'image':dish.image, 
             'price':dish.price,
            'restaurant':dish.resaurant,
         }
         
         return JsonResponse(response_data,status=200)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)
    




'''获取菜品评价'''
#需要返回一个总平均分

@csrf_exempt  #正式上线时去掉
def get_dish_eval(request,dish_id):
    try:
        dish = Dish.objects.get(pk=dish_id)
    except Dish.DoesNotExist:
        return JsonResponse({'error': 'Dish not found'}, status=404)
    
    if request.method == 'GET':
         avg_score = DishEval.objects.filter(dish=dish).aggregate(avg_value=Avg('score'))['avg_value']
         dish_evals = DishEval.objects.filter(dish=dish)
         response = DishEvalSerializer(dish_evals, many=True)
         return JsonResponse({'avg_score':avg_score,'data':response.data},status=200)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)

'''顾客评论/删除评论菜品'''

@csrf_exempt  #正式上线时去掉
def create_dish_eval(request,user_id,dish_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    try:
        dish = Dish.objects.get(pk=dish_id)
    except Dish.DoesNotExist:
        return JsonResponse({'error': 'Dish not found'}, status=404)
    
    if request.method == 'POST':
        # 获取请求体中的数据
        data = json.loads(request.body)
        score = data.get('score', '')
        comment = data.get('comment', '')

        # 创建新的店铺记录
        new_dish_eval = DishEval.objects.create(
            score=score,
            comment=comment,
            dish=dish,
            user=user,
            time=datetime.now(),
        )

        # 构造返回的 JSON 数据
        response_data = {
            'id': new_dish_eval.id,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'message': 'DishEval created successfully',
        }
        
        return JsonResponse(response_data,status=200)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)

@csrf_exempt 
def delete_dish_eval(request,eval_id):
    
    try:
        dish_eval = DishEval.objects.get(pk=eval_id)
    except DishEval.DoesNotExist:
        return JsonResponse({'error': 'DishEval not found'}, status=404)

    if request.method == 'DELETE':
        dish_eval.delete()
        return JsonResponse({'message': 'DishEval deleted successfully'},status=200)
    else:
        return JsonResponse({'error': 'Only DELETE requests are allowed'}, status=405)
    


'''搜索店铺/菜品''' 
@csrf_exempt  #正式上线时去掉
def search(request,name):  
    def common_char(str,wlist):
        list_char=[]
        for w in wlist:
            list_char+=list(w)
        return set(list_char)&set(list(str))
    if request.method == 'GET':
        try:
            sim=TjeatwhatappConfig.model.most_similar(name, topn=10)
            sims=[jieba.lcut(i[0]) for i in sim] #二维列表
            simss=set(item for sublist in sims for item in sublist)
            print(simss)
            expanded_words = list(set(name).union(simss))
            # expanded_words =jieba.lcut(name)
            all_restaurants = Restaurant.objects.all()
            all_dishes=Dish.objects.all()

            # 进行重合字符数计算，并排序
            rest = sorted(
            [r for r in all_restaurants if len(common_char(r.name,expanded_words)) > 0],
            key=lambda r: len(common_char(r.name,expanded_words)),
            reverse=True
            )

            dish = sorted(
            [r for r in all_dishes if len(common_char(r.name,expanded_words)) > 0],
            key=lambda r:len(common_char(r.name,expanded_words)),
            reverse=True
            )
            
            dishes = DishSerializer(dish,many=True)
            rests = RestaurantSerializer(rest,many=True)
            return JsonResponse({'dishes':dishes.data,'rests':rests.data}, status=200)
        except Dish.DoesNotExist and Restaurant.DoesNotExist:
            return JsonResponse({'message':'Can\'t find the dish or restaurant'},status=404)
            
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)




'''顾客查看菜品的评价'''
