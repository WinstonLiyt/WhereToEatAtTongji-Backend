from django.urls import path
from . import views


urlpatterns = [
    path('restaurant/<int:user_id>/create', views.create_restaurant,name="create_restaurant"),
    path('restaurant/<int:rest_id>/update/',  views.update_restaurant,name="update_restaurant"),
    path('restaurant/<int:rest_id>/delete/',  views.delete_restaurant,name="delete_restaurant"),
    path('dish/<int:rest_id>/',views.get_rest,name='get_rest'),
    path('dish/<int:rest_id>/create', views.create_dish,name="create_dish"),
    path('dish/<int:dish_id>/update/',  views.update_dish,name="update_dish"),
    path('dish/<int:dish_id>/delete/',  views.delete_dish,name="delete_dish"),
    path('dish/<int:dish_id>/eval/',views.get_dish_eval,name='get_dish_eval'),
    path('dish/<int:dish_id>/',views.get_dish,name='get_dish'),
    path('restaurant/all/',views.get_all_rest,name='get_all_rest'),
    path('restaurant/<int:rest_id>/all_dish',views.get_all_dish,name='get_all_dish'),
    path('eval/<int:eval_id>/reply/',views.reply,name='reply'),
    path('eval/<int:user_id>/<int:dish_id>/create/',views.create_dish_eval,name='create_dish_eval'),
    path('eval/<int:eval_id>/delete/',views.delete_dish_eval,name='delete_dish_eval'),
    path('search/<str:name>/',views.search,name='search'),
    path('image/',  views.upload_file,name="upload_image"),


    # path('user/login/',  views.UserLogin.as_view()),
    path('user/wx_login/',  views.WeixinLogin.as_view()),
    path('user/test_token/', views.user.TestTokenView.as_view(), name='TestTokenView'),
    
]

