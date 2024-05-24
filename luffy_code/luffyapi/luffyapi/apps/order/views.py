from django.shortcuts import render
from . import models
# Create your views here.
from rest_framework.generics import CreateAPIView
from .serializers import OrderModelSerializer
from rest_framework.permissions import IsAuthenticated
class OrderAPIView(CreateAPIView):
    """订单视图"""
    queryset = models.Order.objects.filter(is_show=True,is_deleted=False)
    serializer_class = OrderModelSerializer
    permission_classes = [IsAuthenticated, ]

    # obj = OrderModelSerializer(instance=, data=,context={})
    # '''
    # {
    #         'request': self.request,
    #         'format': self.format_kwarg,
    #         'view': self
    #     }
    # '''
    # obj.context['request'] = self.request










