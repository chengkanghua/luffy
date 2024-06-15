from django.shortcuts import render
from rest_framework.generics import ListAPIView
# Create your views here.
from . import models
from luffyapi.settings import contants
from . import serializers

from django.contrib.auth.models import User


class BannerAPIView(ListAPIView):
    # 没必要获取所有数据，只需要获取要显示的数据
    queryset = models.Banner.objects.filter(is_deleted=False, is_show=True)[:contants.BANNER_LENGTH]
    serializer_class = serializers.BannerModelSerializer


class NavAPIView(ListAPIView):
    queryset = models.Nav.objects.filter(is_deleted=False, is_show=True,position=1)[:contants.HEADER_NAV_LENGTH]
    serializer_class = serializers.NavModelSerializer

