from django.urls import path
from . import views

urlpatterns = [
    path('user/login/', views.user.UserLogin.as_view(), name='UserLogin'),
    path('user/wx_login/', views.user.WeixinLogin.as_view(), name='WeixinLogin'),
    path('user/test_token/', views.user.TestTokenView.as_view(), name='TestTokenView'),
    ]
#TestTokenView