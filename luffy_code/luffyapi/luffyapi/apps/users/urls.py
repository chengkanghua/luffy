from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path,re_path
from . import views

urlpatterns = [
    path(r'login/', obtain_jwt_token),
    path(r"register/", views.UserAPIView.as_view()),
    path(r'order/list/', views.UserOrderAPIView.as_view()),
    re_path(r"mobile/(?P<mobile>1[3-9]\d{9})/", views.MobileAPIView.as_view()),
    re_path(r'sms/(?P<mobile>1[3-9]\d{9})/', views.SMSAPIView.as_view()),
    path("reg/", views.UserAPIView.as_view()),
]