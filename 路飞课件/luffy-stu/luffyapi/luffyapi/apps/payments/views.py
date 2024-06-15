from django.shortcuts import render,HttpResponse
from alipay import AliPay
# Create your views here.
from rest_framework.views import APIView
from django.conf import settings
from order.models import Order
from rest_framework.response import Response
from rest_framework import status
from coupon.models import UserCoupon
from django.db import transaction
from users.models import UserCourse
from course.models import CourseExpire
from datetime import datetime,timedelta
import logging
logger = logging.getLogger('django')


class AlipayAPIView(APIView):

    def get(self,request):

        order_number = request.query_params.get('order_number')
        try:
            order_obj = Order.objects.get(order_number=order_number)

        except:
            return Response({'msg':'订单号有误，请核实后在发送请求'})

        alipay = AliPay(

            appid=settings.ALIAPY_CONFIG['appid'],
            app_notify_url=None,  # 默认回调url
            app_private_key_string=open(settings.ALIAPY_CONFIG['app_private_key_path']).read(),

            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=open(settings.ALIAPY_CONFIG['alipay_public_key_path']).read(),

            sign_type=settings.ALIAPY_CONFIG['sign_type'],  # RSA 或者 RSA2
            debug = settings.ALIAPY_CONFIG['debug']  # 默认False
        )


        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_number,
            total_amount=float(order_obj.real_price),
            subject=order_obj.order_title,
            return_url=settings.ALIAPY_CONFIG['return_url'],
            notify_url=settings.ALIAPY_CONFIG['notify_url']  # 可选, 不填则使用默认notify url
        )

        url = settings.ALIAPY_CONFIG['gateway_url'] + order_string

        #https://openapi.alipay.com/gateway.do? + order_string

        return Response(url)



class AliPayResultAPIView(APIView):

    def get(self,request):
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG['appid'],
            app_notify_url=None,  # 默认回调url
            app_private_key_string=open(settings.ALIAPY_CONFIG['app_private_key_path']).read(),

            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=open(settings.ALIAPY_CONFIG['alipay_public_key_path']).read(),

            sign_type=settings.ALIAPY_CONFIG['sign_type'],  # RSA 或者 RSA2
            debug=settings.ALIAPY_CONFIG['debug']  # 默认False
        )

        data = request.query_params.dict() #普通字典数据

        signature = data.pop("sign")

        # verification
        # 回复验证结果
        success = alipay.verify(data, signature)
        if success:
            ret = self.change_order_status(data)
            print(ret.status_code)
            return ret
        else:
            return Response({'msg':'支付检验失败！'})


    def post(self,request):
        print('post请求来了！！！！！')
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG['appid'],
            app_notify_url=None,  # 默认回调url
            app_private_key_string=open(settings.ALIAPY_CONFIG['app_private_key_path']).read(),

            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=open(settings.ALIAPY_CONFIG['alipay_public_key_path']).read(),

            sign_type=settings.ALIAPY_CONFIG['sign_type'],  # RSA 或者 RSA2
            debug=settings.ALIAPY_CONFIG['debug']  # 默认False
        )

        data = request.query_params.dict()  # 普通字典数据

        signature = data.pop("sign")

        # verification
        success = alipay.verify(data, signature)
        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            ret = self.change_order_status(data)
            if ret.status_code == 200:
                return HttpResponse('success')
            else:
                return Response({'msg': '支付检验失败！'})
        else:
            return Response({'msg': '支付检验失败！'})


    def change_order_status(self,data):
        # 更改订单状态，改为已支付
        order_number = data.get("out_trade_no")
        print(order_number)
        try:
            order_obj = Order.objects.get(order_number=order_number, order_status=0)

        except Order.DoesNotExist:
            return Response({'msg': '查询不到订单'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                sid = transaction.savepoint()
                order_obj.order_status = 1
                order_obj.save()

                # 用户使用的优惠券状态修改
                coupon_id = order_obj.coupon
                if coupon_id > 0:
                    user_coupon = UserCoupon.objects.get(pk=coupon_id, is_use=False, is_show=True, is_deleted=False)
                    user_coupon.is_use = True
                    user_coupon.save()

                # 用户使用的积分要扣除
                use_credit = order_obj.credit
                user_obj = order_obj.user
                if use_credit > 0:
                    user_obj.credit -= use_credit
                    user_obj.save()

                course_list = []
                # 找到该订单的所有课程信息
                order_course_list = order_obj.order_courses.all()
                for order_detail in order_course_list:
                    course = order_detail.course
                    course.students += 1
                    course.save()

                    course_list.append({
                        "id":course.id,
                        'name':course.name
                    })

                    pay_time = order_obj.pay_time
                    expire_id = order_detail.expire

                    if expire_id > 0:
                        expire_obj = CourseExpire.objects.get(pk=expire_id)

                        out_time = pay_time + timedelta(days=expire_obj.expire_time)

                    else:
                        out_time = None

                    # 支付宝的流水号要记录  （购买记录表，）
                    UserCourse.objects.create(
                        user_id=user_obj.id,
                        course_id=course.id,
                        trade_no=data.get('trade_no'),
                        buy_type=1,
                        pay_time=pay_time,
                        out_time=out_time,
                    )
        except:
            logger.error('订单更新失败！！！！')
            transaction.savepoint_rollback(sid)
            return Response({'msg': '更新订单相关记录失败，请重试'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'msg': '支付成功了',
            'course_list':course_list,
            'pay_time':order_obj.pay_time,
            'real_price':order_obj.real_price
        })





