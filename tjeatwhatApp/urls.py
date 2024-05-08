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
