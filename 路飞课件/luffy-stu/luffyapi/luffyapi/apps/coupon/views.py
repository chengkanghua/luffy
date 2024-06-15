from django.shortcuts import render

# Create your views here.

from . import models
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CouponModelSerializer,UserCouponModelSerializer
class UserCouponAPIView(ListAPIView):
    # queryset = models.UserCoupon.objects.filter(is_show=True,is_deleted=False,is_use=False,)

    serializer_class = UserCouponModelSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        #self
        # print('xxxxxxxxxx',models.UserCoupon.objects.filter(is_show=True,is_deleted=False,is_use=False,user_id=self.request.user.id))
        return models.UserCoupon.objects.filter(is_show=True,is_deleted=False,is_use=False,user_id=self.request.user.id)







