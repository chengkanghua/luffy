
from rest_framework import serializers

from coupon.models import UserCoupon
from . import models
from datetime import datetime
from django_redis import get_redis_connection
from course.models import CourseExpire
from course.models import Course
from django.db import transaction
from datetime import datetime
# from coupon.models import UserCoupon,Coupon
from rest_framework.response import Response
from rest_framework import status
from luffyapi.settings import constants


class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['id', 'order_number', 'pay_type', 'credit', 'coupon']
        extra_kwargs = {
            'id': {'read_only': True},
            'order_number': {'read_only': True},
            'pay_type': {'write_only': True},
            'credit': {'write_only': True},
            'coupon': {'write_only': True},
        }


    def validate(self, attrs):
        pay_type = attrs.get("pay_type")
        try:
            models.Order.pay_choices[pay_type]
        except:
            raise serializers.ValidationError('抱歉，选择的支付方式有误！！')

        # todo 验证积分上限
        #获取到用户最大积分量
        max_credit = self.context['request'].user.credit
        #获取用户使用了多少积分
        credit = attrs.get("credit",0)

        #判断使用积分不能大于最大积分量
        if credit != 0 and credit > max_credit:
            raise serializers.ValidationError('抱歉，积分超过上限，不要搞事情！')

        # todo 验证优惠券是否在有效期内
        use_coupon_id = attrs.get("coupon")
        if use_coupon_id > 0:
            now = datetime.now()

            try:
                user_coupon = UserCoupon.objects.get(is_show=True,is_deleted=False,is_use=False,pk=use_coupon_id,user_id=self.context["request"].user.id)
            except:
                raise serializers.ValidationError('当前优惠券不存在或者不能使用')

            s_time = user_coupon.start_time.timestamp()
            e_time = user_coupon.end_time.timestamp()
            now_stamp = now.timestamp()
            if now_stamp < s_time or now_stamp > e_time:
                raise serializers.ValidationError('当前优惠券还不能使用或者已经过期')




        # todo 校验课程是否存在

        return attrs


    def create(self, validated_data):
        # 订单号生成[时间日期 + 用户id + 自增值]
        redis_conn = get_redis_connection('cart')

        user_id = self.context['request'].user.id
        user_coupon_id = validated_data.get('coupon',0)
        pay_type = validated_data.get('pay_type')
        credit = validated_data.get('credit', 0)

        # 1 -- 10000000
        incr = redis_conn.incr("order")  #redis自增
        # print(incr,type(incr)) # 1 int
        current_time = datetime.now()
        order_number = current_time.strftime('%Y%m%d%H%M%S') + "%06d" % user_id + "%06d" % incr

        pipe = redis_conn.pipeline()
        pipe.multi()
        with transaction.atomic():  # 事务开始
            sid = transaction.savepoint()  # 设置事务回滚标记点
            order = models.Order.objects.create(**{  #basemodel created_time
                'order_title':'路飞学成xx课程购买',
                'total_price':0,
                'real_price':0,
                'order_number':order_number,
                'order_status':0,
                'pay_type':pay_type,
                'credit':credit,
                'coupon':user_coupon_id,
                'order_desc':'',
                'pay_time':current_time,
                'user_id':user_id,
            })

            #生成订单详情数据
            cart_data_dict = redis_conn.hgetall("cart_%s" % user_id)
            selected_course_data = redis_conn.smembers("selected_%s" % user_id)

            real_p = 0  #真实价格总计
            total_p = 0 #原价总计
            for course_id_bytes, expire_bytes in cart_data_dict.items():
                course_id = int(course_id_bytes.decode())
                expire_id = int(expire_bytes.decode())
                if course_id_bytes in selected_course_data:
                    try:
                        course_obj = Course.objects.get(pk=course_id)
                    except:
                        continue
                    try:
                        if expire_id > 0:
                            expire_obj = CourseExpire.objects.get(is_show=True, is_deleted=False, id=expire_id)

                    except CourseExpire.DoesNotExist:
                        transaction.savepoint_rollback(sid)
                        # print(order)
                        # return Response({'msg': '有效期不存在！'}, status=status.HTTP_400_BAD_REQUEST)
                        raise serializers.ValidationError('有效期不存在')

                    origin_price = course_obj.price
                    real_price = course_obj.real_price(expire_id)
                    discount_name = course_obj.discount_name
                    models.OrderDetail.objects.create(**{
                        'order':order,
                        'course':course_obj,
                        'expire':expire_id,
                        'price':origin_price,
                        'real_price':real_price,
                        'discount_name':discount_name,
                    })

                    total_p += float(origin_price)
                    # order.total_price += float(origin_price)
                    real_p += float(real_price)
                # order.real_price += float(real_price)

                    #当生成订单之后，就把购物车里面的选中的数据给删除掉，没有什么用了
                    pipe.hdel("cart_%s" % user_id, course_id)
                    pipe.srem("selected_%s" % user_id, course_id)


            print('>>>real_p',real_p)
            print('>>>total_p',total_p)

            # 优惠券计算
            if user_coupon_id > 0:
                try:
                    user_coupon_obj = UserCoupon.objects.get(pk=user_coupon_id)
                    if user_coupon_obj.coupon.condition > real_p:
                        transaction.savepoint_rollback(sid)
                        raise serializers.ValidationError('订单生成失败，原因是真实价格小于了使用优惠券的价格上限')

                    sale = user_coupon_obj.coupon.sale
                    sale_num = float(sale[1:])
                    if sale[0] == "*":
                        real_p = real_p * sale_num
                    else:
                        real_p = real_p - sale_num
                except:
                    transaction.savepoint_rollback(sid)
                    raise serializers.ValidationError('订单生成失败，原因是真实价格小于了使用优惠券的价格上限')


            #积分计算
            if credit > 0:
                if credit > real_p * constants.CREDIT_MONEY:
                    transaction.savepoint_rollback(sid)
                    raise serializers.ValidationError('对不起，订单生成失败，积分量超过了真实价格，请重新发送请求')

                real_p = float("%.2f" % (real_p - credit / constants.CREDIT_MONEY))


            order.total_price = total_p
            order.real_price = real_p


        try:
            pipe.execute()
            order.save()
        except:
            transaction.savepoint_rollback(sid)  #事务出错回滚点 sid
            raise serializers.ValidationError('订单生成失败！')


        return order















