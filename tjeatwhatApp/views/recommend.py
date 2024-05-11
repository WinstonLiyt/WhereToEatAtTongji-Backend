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

#随机推荐——获取所有商店getAllStore
@api_view(['GET'])
@authentication_classes([JwtQueryParamsAuthentication])
def get_all_store(request):
    stores = restaurantmodels.Restaurant.objects.all()
    store_list = []
    for store in stores:
        store_list.append({
            'id': store.id,
            'name': store.name
        })

    return Response({
        'stores': store_list
    })
    

#随机推荐——根据餐厅id获取所有菜品getAllDish
@api_view(['GET'])
@authentication_classes([JwtQueryParamsAuthentication])
def get_all_dish_by_store_id(request):
    
    # 获取查询参数中的 store_id
    store_id = request.GET.get('store_id')
    print("store_id=",store_id)
    dishes = dishmodels.Dish.objects.filter(restaurant_id=store_id)
    # 从数据库中获取相应 store_id 的所有菜品
    # restaurant=restaurantmodels.Restaurant.objects.filter(id=store_id)
    # print("resturant_id=",restaurant.id)
    # 假设 restaurant 是一个 Restaurant 对象
    # dishes = dishmodels.Dish.objects.filter(restaurant__id=restaurant.id)
    # print("dishes:",dishes)
    # 构造响应数据
    dish_list = []
    for dish in dishes:
        dish_list.append({
            'id': dish.id,
            'name': dish.name
        })

    # 返回响应
    return Response({
        'dishes': dish_list
    })


#个性化推荐菜品
@api_view(['GET'])
@authentication_classes([JwtQueryParamsAuthentication])
def get_dish_by_user_interest(request):
    user_id=request.user.get('id')
     
    
    # 查询所有属于指定用户且评分大于等于4的DishEval对象
    dish_evals = dishmodels.DishEval.objects.filter(user_id=user_id, score__gte=4)

    # 获取这些DishEval对象对应的菜品对象
    interest_dishes = [eval.dish for eval in dish_evals]
    #获取这些菜品的名称
    interest_dish_names = [dish.name for dish in interest_dishes]
    #获取这些菜品的id
    interest_dish_ids = [dish.id for dish in interest_dishes]
    print("interest_dish_names=",interest_dish_names)
    recommend_dishes_id = []
    recommend_dishes_id.extend(interest_dish_ids)
    for name in interest_dish_names:
        print("name=",name)
        similar_dish_names = TjeatwhatappConfig.model.most_similar(name, topn=10)
        # 提取相似菜品名称列表
        similar_dish_names = [name[0] for name in similar_dish_names]
        print("similar_dish_names=",similar_dish_names)
        # 查询数据库，找到与相似菜品名称匹配的菜品对象
        similar_dishes = dishmodels.Dish.objects.filter(name__in=similar_dish_names)
        # 提取相似菜品的ID列表
        similar_dish_ids = [dish.id for dish in similar_dishes]
        recommend_dishes_id.extend(similar_dish_ids)

    print("recommend_dishes_id=",recommend_dishes_id)

    # 去除重复的菜品ID
    recommend_dishes_id = list(set(recommend_dishes_id))
    #从recommend_dishes_id中随机选择一条
    random_dish_id = random.choice(recommend_dishes_id)
    

    
    # 查询数据库，找到与随机选择的菜品ID匹配的菜品对象
    recommend_dish = dishmodels.Dish.objects.get(id=random_dish_id)
    
    # 如果找到了菜品，则构造响应数据
    if recommend_dish:
        # 获取菜品的标签
        # tags = [tag.name for tag in recommend_dish.tags.all()]

        # 获取菜品所属店家的信息
        restaurant_name = recommend_dish.restaurant.name
        dish_description = recommend_dish.description

        dish_data = {
            'id': recommend_dish.id,
            'name': recommend_dish.name,
            # 'tags': tags,
            'store_name': restaurant_name,
            'description': dish_description,
            'img_url': '**/**',
            'price': recommend_dish.price  # 将 DecimalField 转换为字符串
            
            
            # 其他字段根据需要添加
        }
        return Response({'dish': dish_data})
    else:
        return Response({'error': 'No dishes available'}, status=404)

    # # 从 Dish 表中随机抽选一条记录
    # dish = dishmodels.Dish.objects.order_by('?').first()
    # # 如果找到了菜品，则构造响应数据
    # if dish:
    #     # 获取菜品的标签
    #     tags = [tag.name for tag in dish.tags.all()]

    #     # 获取菜品所属店家的信息
    #     restaurant_name = dish.restaurant.name
    #     dish_description = dish.description

    #     dish_data = {
    #         'id': dish.id,
    #         'name': dish.name,
    #         'tags': tags,
    #         'store_name': restaurant_name,
    #         'description': dish_description,
    #         'img_url': '**/**',
    #         'price': dish.price  # 将 DecimalField 转换为字符串
            
            
    #         # 其他字段根据需要添加
    #     }
    #     return Response({'dish': dish_data})
    # else:
    #     return Response({'error': 'No dishes available'}, status=404)