from django.urls import path,re_path
from . import views


urlpatterns = [
    path("banner/",views.BannerListAPIView.as_view()),
    path("nav/header/", views.HeaderNavListAPIView.as_view()),
]