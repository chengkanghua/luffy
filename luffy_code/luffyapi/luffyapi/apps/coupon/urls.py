from django.urls import path,re_path
from . import views

urlpatterns = [
    path(r'', views.UserCouponAPIView.as_view()),
]