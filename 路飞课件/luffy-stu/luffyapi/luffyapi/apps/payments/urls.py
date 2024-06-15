
from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path,re_path
from . import views
urlpatterns = [
    path(r'alipay/', views.AlipayAPIView.as_view()),
    path(r'alipay/result/', views.AliPayResultAPIView.as_view()),


]
