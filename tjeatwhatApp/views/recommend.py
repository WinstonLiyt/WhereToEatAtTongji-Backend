from django.conf import settings

from weixin import WXAPPAPI
from weixin.oauth2 import OAuth2AuthExchangeError
from tjeatwhatApp.extensions.auth import JwtQueryParamsAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from tjeatwhatApp.models import usermodels,dishmodels,restaurantmodels
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes

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
def get_all_dish_by_store_id(request, store_id):
    # 从数据库中获取相应 store_id 的所有菜品
    dishes = dishmodels.Dish.objects.filter(restaurant_id=store_id)
    
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
    # 从 Dish 表中随机抽选一条记录
    dish = dishmodels.Dish.objects.order_by('?').first()
    # 如果找到了菜品，则构造响应数据
    if dish:
        # 获取菜品的标签
        tags = [tag.name for tag in dish.tags.all()]

        # 获取菜品所属店家的信息
        restaurant_name = dish.restaurant.name
        dish_description = dish.description

        dish_data = {
            'id': dish.id,
            'name': dish.name,
            'tags': tags,
            'store_name': restaurant_name,
            'description': dish_description,
            'img_url': '**/**',
            'price': dish.price  # 将 DecimalField 转换为字符串
            
            
            # 其他字段根据需要添加
        }
        return Response({'dish': dish_data})
    else:
        return Response({'error': 'No dishes available'}, status=404)