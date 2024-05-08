from django.urls import path
from . import views


urlpatterns = [
    path('restaurant/create', views.create_restaurant,name="create_restaurant"),
    path('restaurant/<int:id>/update/',  views.update_restaurant,name="update_restaurant"),
    path('restaurant/<int:id>/delete/',  views.delete_restaurant,name="delete_restaurant"),
    path('restaurant/<int:id>/create', views.create_dish,name="create_dish"),
    path('restaurant/<int:id>/<int:dish_id>/update/',  views.update_dish,name="update_dish"),
    path('restaurant/<int:id>/<int:dish_id>/delete/',  views.delete_dish,name="delete_dish"),
    path('image/',  views.upload_file,name="upload_image"),
    
    #zrx
    path('user/wx_login/', views.user.WeixinLogin.as_view(), name='WeixinLogin'),
    path('user/test_token/', views.test_token_view, name='TestTokenView'),
    path('recomend/getAllStore/', views.recommend.getAllStore.as_view(), name='getAllStore'),
    path('recomend/getAllDishByStoreID/<int:store_id>/', views.recommend.getAllDishByStoreID.as_view(), name='getAllDishByStoreID'),
]
