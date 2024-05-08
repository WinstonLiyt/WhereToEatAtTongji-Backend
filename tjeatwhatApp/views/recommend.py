from django.conf import settings

from weixin import WXAPPAPI
from weixin.oauth2 import OAuth2AuthExchangeError
from tjeatwhatApp.extensions.auth import JwtQueryParamsAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from tjeatwhatApp.models import usermodels,dishmodels,restaurantmodels
from rest_framework import status

#随机推荐——获取所有商店getAllStore
class getAllStore(APIView):
    authentication_classes = []
    def get(self,request):
        stores = restaurantmodels.Restaurant.objects.all()
        store_list = []
        for store in stores:
            store_list.append({
                'id':store.id,
                'name':store.name
            })

        return Response({
            'stores':store_list
        })
    

#随机推荐——根据餐厅id获取所有菜品getAllDish
class getAllDishByStoreID(APIView):
    authentication_classes = []
    def get(self,request,store_id):
        #print("request.data:",request.data)
        #store_id = request.data.get('store_id')
        # if store_id is None:
        #     return Response({'error': 'Missing store_id in request body'}, status=status.HTTP_400_BAD_REQUEST)

        dishes = dishmodels.Dish.objects.filter(restaurant_id=store_id)
        dish_list = []
        for dish in dishes:
            dish_list.append({
                
                'id':dish.id,

                'name':dish.name
            })
        
        return Response({
            'dishes':dish_list
        })