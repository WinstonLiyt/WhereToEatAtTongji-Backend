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
    path('restaurant/<int:rest_id>/all_dish/',views.get_all_dish,name='get_all_dish'),
    path('eval/<int:eval_id>/reply/',views.reply,name='reply'),
    path('eval/<int:user_id>/<int:dish_id>/create/',views.create_dish_eval,name='create_dish_eval'),
    path('eval/<int:eval_id>/delete/',views.delete_dish_eval,name='delete_dish_eval'),
    path('search/<str:name>/',views.search,name='search'),
    path('image/',  views.upload_file,name="upload_image"),


    
    #zrx
    path('user/login', views.login, name='login'),
    path('user/studentRegister', views.student_register, name='student_register'),
    path('user/storeRegister',views.store_register, name='store_register'),
    path('user/test_token', views.test_token_view, name='TestTokenView'),
    path('user/setName', views.set_name, name='set_name'),
    path('user/setSignature', views.set_signature, name='set_signature'),

    path('user/avatar', views.set_avatar, name='set_avatar'),
    path('user/getInfo',views.get_user_info,name='get_user_info'),
    path('user/uploadAvatar',views.upload_avatar,name='upload_avatar'),

    path('recommend/getAllStore', views.get_all_store, name='get_all_store'),
    path('recommend/getAllDishesByStoreID/', views.get_all_dish_by_store_id, name='getAllDishesByStoreID'),
    path('recommend/getPersonalDish', views.get_dish_by_user_interest, name='get_dish_by_user_interest'),

    # gaq
    path('posts/search/', views.search_posts, name='search_posts'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/delete/', views.delete_post, name='delete_post'),
    path('posts/comment/', views.comment_post, name='comment_post'),
    path('posts/details/', views.get_one_post, name='get_one_post'),
    path('posts/getcomments/', views.get_one_comment, name='get_one_comment'),
    path('posts/reply_comment/', views.reply_comment, name='reply_comment'),
    path('posts/change_post_reaction/', views.change_post_reaction, name='change_reaction'),
    path('posts/delete_comment/', views.delete_comment, name='delete_comment'),
    path('posts/change_comment_reaction/', views.change_comment_reaction, name='delete_reply'),
    # path('uploads/', views.upload_image, name='upload_image'),
    # path('create/', views.create_user, name='create_user'),
]