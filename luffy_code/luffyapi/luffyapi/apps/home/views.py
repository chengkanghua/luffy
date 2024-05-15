from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from .models import Banner
from .serializers import BannerModelSerializer
from luffyapi.settings import constants

class BannerListAPIView(ListAPIView): # 自动导包
    queryset = Banner.objects.filter(is_show=True, is_deleted=False).order_by("-orders","-id")[:constants.BANNER_LENGTH] #没有必要获取所有图片数据，因为有些可能是删除了的、或者不显示的
    # 切片获取数据的时候，我们可以将切片长度设置成配置项
    serializer_class = BannerModelSerializer