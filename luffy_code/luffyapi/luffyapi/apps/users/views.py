
from django.shortcuts import render

# Create your views here.

from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from .models import User
from .serializers import UserModelSerializer
class UserAPIView(CreateAPIView):
    """用户信息视图"""
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

import re
from rest_framework import status
from .utils import get_user_by_account
from rest_framework.response import Response

class MobileAPIView(APIView):
    def get(self,request,mobile):
        ret = get_user_by_account(mobile)
        if ret is not None:
            return Response({"message":"手机号已经被注册过！"},status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({"message":"这个号码可以被注册"})



import random
from luffyapi.settings import constants
from django_redis import get_redis_connection
from .utils import send_message
import logging
logger = logging.getLogger('django')
#理论来说，我们是不需要什么数据库处理的，所以我们直接继承APIView就可以了
class SMSAPIView(APIView):
    """
    发送短信
    """
    def get(self,request,mobile):

        try:
            # 引入redis
            redis = get_redis_connection("sms_code")

            # 判断当前手机号码是否曾经在60s发送过短信
            mobile_intervel = redis.get("mobile_%s" % mobile)
            if mobile_intervel:
                return Response({"result":"对不起~手机短信发送间隔不足1分钟!"},status=status.HTTP_400_BAD_REQUEST)

            # 在以后开发中如果一次性要写入多条redis命令，建议采用管道操作[事务操作]来把多条数据整理成一块，一并发送给redis
            pip = redis.pipeline()
            pip.multi()

            # 设置短信发送间隔时间
            # setex mobile_17776445415 60 _
            pip.setex("mobile_%s" % mobile, constants.SMS_INTERVAL_TIME,"_") # "_" 表示占位符，没有任何意义的

            # 生成短信号码并把短信和手机号码保存到redis中
            code = "%04d" % random.randint(0, 9999)

            # 可以使用string格式进行数据保存
            # setex sms_17776445415 300 666666
            pip.setex("sms_%s" % mobile, constants.SMS_EXPIRE_TIME,code)

            # 执行管道中的所有命令[提交事务]
            pip.execute()

            # 发送短信
            # send_message("模板id",'手机号码,',datas = ('验证码1-4位', '有效时间'))
            # 短信模板ID 在测试阶段是1
            datas = (code, constants.SMS_EXPIRE_TIME // 60)
            result = send_message(constants.SMS_TEMPLATE_ID,mobile,datas)
            if result == 0:
                logger.error("发送短信出错！手机号：%s" % mobile)
                return Response({"status":"0","result":"短信发送失败！"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error("发送短信出错！%s" % e)
            return Response({"status":"0","result":"服务器发送短信有误！"},status=status.HTTP_507_INSUFFICIENT_STORAGE)

        return Response({"status":"1","result":"短信发送成功！"},status=status.HTTP_200_OK)



from rest_framework.generics import CreateAPIView
from .serializers import UserModelSerializer
class UserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer







