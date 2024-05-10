from django.urls import path
from . import views


urlpatterns = [
    path('restaurant/<int:user_id>/create/', views.create_restaurant,name="create_restaurant"),
    path('restaurant/<int:rest_id>/update/',  views.update_restaurant,name="update_restaurant"),
    path('restaurant/<int:rest_id>/delete/',  views.delete_restaurant,name="delete_restaurant"),
    path('restaurant/<int:rest_id>/',views.get_rest,name='get_rest'),
    path('dish/<int:rest_id>/create/', views.create_dish,name="create_dish"),
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


    
    #zrx
    path('user/login/', views.login, name='login'),
    path('user/studentRegister/', views.student_register, name='student_register'),
    path('user/storeRegister/',views.store_register, name='store_register'),
    path('user/test_token/', views.test_token_view, name='TestTokenView'),
    path('user/setName/', views.set_name, name='set_name'),
    path('user/avatar/', views.set_avatar, name='set_avatar'),
    
    path('recomend/getAllStore/', views.get_all_store, name='get_all_store'),
    path('recomend/getAllDishByStoreID/<int:store_id>/', views.get_all_dish_by_store_id, name='getAllDishByStoreID'),
    path('recomend/getPersonalDish', views.get_dish_by_user_interest, name='get_dish_by_user_interest')
]

