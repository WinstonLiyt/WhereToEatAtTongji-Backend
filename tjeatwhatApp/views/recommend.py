from django.conf import settings
from ..apps import TjeatwhatappConfig
from weixin import WXAPPAPI
from weixin.oauth2 import OAuth2AuthExchangeError
from tjeatwhatApp.extensions.auth import JwtQueryParamsAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response 
from tjeatwhatApp.models import usermodels,dishmodels,restaurantmodels

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
import random
import requests



#随机推荐——获取所有商店getAllStore
@api_view(['GET'])
def get_all_store(request):
    stores = restaurantmodels.Restaurant.objects.all()
    if stores:
        store_list = []
        for store in stores:
            dishes = dishmodels.Dish.objects.filter(restaurant_id=store.id)
            if dishes:
                store_list.append({
                    'id': store.id,
                    'name': store.name
                })

        return Response({'stores': store_list},status=200)
    
    return Response({'error': '餐厅表为空'}, status=404)
    

#随机推荐——根据餐厅id获取所有菜品getAllDish
@api_view(['GET'])
def get_all_dish_by_store_id(request):

    store_id = request.GET.get('store_id')
    if store_id:
        dishes = dishmodels.Dish.objects.filter(restaurant_id=store_id)
        if dishes:
            dish_list = []
            for dish in dishes:
                dish_list.append({
                    'id': dish.id,
                    'name': dish.name
                })
            else:
                return Response({'dishes': dish_list},status=200)
        else:
            return Response({'error': '未找到该餐厅'}, status=404)
    return Response({'error': '获取餐厅id失败'}, status=400)


#个性化推荐菜品
@api_view(['GET'])
@authentication_classes([JwtQueryParamsAuthentication])
def get_dish_by_user_interest(request):

    user_id=request.user.get('id')
    print("userid",user_id)
    # 查询所有属于指定用户且评分大于等于4的DishEval对象
    dish_evals = dishmodels.DishEval.objects.filter(user_id=user_id, score__gte=4)
    # 获取这些DishEval对象对应的菜品对象
    if dish_evals:
        interest_dishes = [eval.dish for eval in dish_evals]
        #获取这些菜品的名称
        interest_dish_names = [dish.name for dish in interest_dishes]
        #获取这些菜品的id
        interest_dish_ids = [dish.id for dish in interest_dishes]
        # print("interest_dish_names=",interest_dish_names)
        recommend_dishes_id = []
        recommend_dishes_id.extend(interest_dish_ids)
        for name in interest_dish_names:
            print("name=",name)
            url = 'http://localhost:5000/model/'

            # 发送 GET 请求并获取响应
            # name='包子'
            response = requests.get(url, params={'name': name}).json()
            # print("response:",response)
            similar_dish_names = response['sim']
            # 提取相似菜品名称列表
            similar_dish_names = [name[0] for name in similar_dish_names]
            # print("similar_dish_names=",similar_dish_names)
            # 查询数据库，找到与相似菜品名称匹配的菜品对象
            similar_dishes = dishmodels.Dish.objects.filter(name__in=similar_dish_names)
            # 提取相似菜品的ID列表
            similar_dish_ids = [dish.id for dish in similar_dishes]
            recommend_dishes_id.extend(similar_dish_ids)

        # 去除重复的菜品ID
        recommend_dishes_id = list(set(recommend_dishes_id))
        
        #从recommend_dishes_id中随机选择一条
        random_dish_id = random.choice(recommend_dishes_id)

    #若用户没有评分记录
    else:
        all_dishes=dishmodels.Dish.objects.all()
        if not all_dishes:
            return Response({'error':"菜品表为空"},status=404)
        
        all_dishes_id=[]
        for dish in all_dishes:
            all_dishes_id.append(dish.id)

        random_dish_id = random.choice(all_dishes_id)

    # print("random_dish_id:",random_dish_id)
    # 查询数据库，找到与随机选择的菜品ID匹配的菜品对象
    
    recommend_dish = dishmodels.Dish.objects.get(id=random_dish_id)

    # 如果找到了菜品，则构造响应数据
    if recommend_dish:
        # 获取菜品所属店家的信息

        dish_data = {
            'id': recommend_dish.id,
            'name': recommend_dish.name,
            'store_name': recommend_dish.restaurant.name,
            'description': recommend_dish.description,
            'img_url': str(recommend_dish.image),
            'price': recommend_dish.price  
        }
        return Response(dish_data,status=200)
    else:
        return Response({'error': '没有相关推荐的菜品'}, status=404)
        
        

    