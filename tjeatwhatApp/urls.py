from django.urls import path
from . import views


urlpatterns = [
    path('restaurant/', views.create_restaurant,name="create_restaurant"),
    path('restaurant/<int:id>/update',  views.update_restaurant,name="update_restaurant"),
    path('restaurant/<int:id>/delete',  views.delete_restaurant,name="delete_restaurant"),
    path('dish/<int:id>/', views.create_dish,name="create_dish"),
    path('dish/<int:id>/<int:dish_id>/update',  views.update_dish,name="update_dish"),
    path('dish/<int:id>/<int:dish_id>/delete',  views.delete_dish,name="delete_dish"),
    path('image/',  views.upload_file,name="upload_image"),
    
]