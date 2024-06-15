from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
# Create your views here.
from .geetest import GeetestLib
from rest_framework.response import Response
from .utils import get_user_by_account
from rest_framework import status
from . import models
from order.models import Order
import logging
logger = logging.getLogger('django')

pc_geetest_id = "8845ffc862dc0597b30f78831369a27b"
pc_geetest_key = "2dc2dde1477594e1aebc5534ba3c080f"

class CaptchaAPIView(APIView):
    user_id = 'test'  # 用户名
    status = 1
    def get(self,request):
        username = request.query_params.get('username')
        user = get_user_by_account(username)
        if user is None:
            return Response({'msg':'你这啥用户，根本找不到！'},status=status.HTTP_400_BAD_REQUEST)

        self.user_id = user.id

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)

        #todo user_id和stutas保存到另外一个地方，比如redis
        #status ：1成功，0失败
        # request.session[gt.GT_STATUS_SESSION_KEY] = status
        # request.session["user_id"] = user_id

        response_str = gt.get_response_str()
        return HttpResponse(response_str)

    def post(self,request):
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        # challenge = request.POST.get(gt.FN_CHALLENGE, '')
        # validate = request.POST.get(gt.FN_VALIDATE, '')
        # seccode = request.POST.get(gt.FN_SECCODE, '')
        # status = request.session[gt.GT_STATUS_SESSION_KEY]
        # user_id = request.session["user_id"]
        challenge = request.data.get(gt.FN_CHALLENGE, '')
        #geetest_challenge
        validate = request.data.get(gt.FN_VALIDATE, '')
        seccode = request.data.get(gt.FN_SECCODE, '')

        if self.status:
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status":"success"} if result else {"status":"fail"}
        return Response(result)

from rest_framework.generics import CreateAPIView
from .serializers import UserModelSerializer
from rest_framework.views import APIView
from .utils import get_user_by_account

class UserAPIView(CreateAPIView):
    """注册新用户接口"""
    queryset = models.User.objects.all()
    serializer_class = UserModelSerializer



class MobileAPIView(APIView):
    def get(self,request,mobile):

        user = get_user_by_account(mobile)
        if user is not None:
            return Response({'msg':'抱歉，手机号已经被注册过了'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'ok'})


import random
from django_redis import get_redis_connection
from luffyapi.settings import contants
from luffyapi.libs.yuntongxun.sms import CCP


class MSMAPIView(APIView):
    def get(self,request,mobile):
        # 首先查看一下该手机号是否已经在60秒内发送过短信了
        redis_conn = get_redis_connection('sms_code')

        check_ret = redis_conn.get('mobile_%s' % mobile)
        # 找不到默认返回的是None
        if check_ret is not None:
            return Response({'msg':'60秒内已经发送过短信了，请稍后尝试！'},status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. 生成验证码,6位的
            sms_code = "%06d" % random.randint(0,999999)
            pipe = redis_conn.pipeline()
            pipe.multi()  #开启批量操作


            # 2. 保存验证码
            pipe.setex('sms_%s' % mobile, contants.SMS_EXPIRE_TIME, sms_code) #--setex k 60 v
            # redis_conn.setex('sms_%s' % mobile, contants.SMS_EXPIRE_TIME, sms_code) #--setex k 60 v

            # 短信发送的时间间隔
            pipe.setex('mobile_%s' % mobile, contants.SMS_INTERVAL_TIME, '_')

            # redis_conn.setex('mobile_%s' % mobile, contants.SMS_INTERVAL_TIME, '_')

            # 执行
            pipe.execute()

            # 3.调用短信发送的SDK来发送短信
            from mycelery.sms.tasks import send_sms

            send_sms.delay(mobile, sms_code)

            # ccp = CCP()
            # # to, datas, temp_id
            # #'15914397060', ['1234',"5"], 1 #"5"是分钟数
            # ret = ccp.send_template_sms('13833013278', [sms_code,contants.SMS_EXPIRE_TIME//60], 1)
            #
            # print('ret>>>',ret)
            # if not ret:
            #     logger.error("%s 发送短信失败" % mobile)
            #     return Response({'msg': '短信发送失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'msg': '发送短信成功！'})

        except :
            return Response({'msg': '内部错误'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserOrderModelSerializer
class UserOrderAPIView(ListAPIView):

    permission_classes = [IsAuthenticated,]
    serializer_class = UserOrderModelSerializer
    def get_queryset(self):

        return Order.objects.filter(user_id=self.request.user.id)










