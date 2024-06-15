from django.shortcuts import render
from rest_framework.viewsets import ViewSet
# Create your views here.
from course import models
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework import status
import logging
logger = logging.getLogger('django')
from rest_framework.permissions import IsAuthenticated
from luffyapi.settings import contants
class CarTAPIView(ViewSet):

    permission_classes = [IsAuthenticated, ]

    def add(self,request):
        """添加购物车数据"""
        course_id = request.data.get('course_id')

        user_id = request.user.id
        # user_id = 1
        #给有效期和是否被选中，设置默认值

        expire = 0  # 0代表永久有效
        is_selected = True  #True代表选中了，默认让用户加入购物车的商品处于选中状态
        try:

            models.Course.objects.get(pk=course_id)
        except models.Course.DoesNotExist:

            return Response({'msg':'商品不存在，请重新添加！'},status=status.HTTP_400_BAD_REQUEST)


        redis_conn = get_redis_connection('cart')

        try:
            pipe = redis_conn.pipeline()
            pipe.multi()
            pipe.hset("cart_%s" % user_id, course_id, expire)
            pipe.sadd("selected_%s" % user_id, course_id)

            pipe.execute()

            course_len = redis_conn.hlen("cart_%s" % user_id)

        except:
            logger.error('购物车添加数据失败了')
            return Response({'msg':'购物车添加失败'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)


        return Response({'msg':'添加成功','course_len':course_len})


    def cart_list(self,request):
        """购物车数据展示"""
        user_id = request.user.id
        # user_id = 1
        redis_conn = get_redis_connection('cart')

        cart_data_dict = redis_conn.hgetall("cart_%s" % user_id)
        selected_course_data = redis_conn.smembers("selected_%s" % user_id)
        # print('>>>',cart_data_dict)
        # print('>>>',selected_course_data)
        '''
        >>> {b'1': b'0', b'29': b'0', b'2': b'0'}
        >>> {b'2', b'1', b'29'}
        '''
        data = []
        try:
            for course_id_bytes, expire_bytes in cart_data_dict.items():
                course_id = int(course_id_bytes.decode())
                expire_id = int(expire_bytes.decode())

                course_obj = models.Course.objects.get(pk=course_id)

                data.append({
                    'id':course_obj.id,
                    'course_img':contants.SERVER_HOST + course_obj.course_img.url,
                    'name':course_obj.name,
                    'origin_price':course_obj.price,
                    'real_price':course_obj.real_price(expire_id),
                    'expire_id':expire_id,
                    'expire_list':course_obj.expire_list,
                    'is_selected':course_id_bytes in selected_course_data,

                })
        except:
            return Response('获取课程数据失败',status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data)


    def change_course_selected(self,request):
        """改变课程勾选状态"""
        user_id = request.user.id
        course_id = request.data.get('course_id')
        #True表示给select_user_id的redis数据中添加一条记录，False表示删除一条记录
        is_selected = request.data.get('is_selected')

        try:
            models.Course.objects.get(pk=course_id)
        except models.Course.DoesNotExist:

            return Response({'msg': '商品不存在！'}, status=status.HTTP_400_BAD_REQUEST)

        redis_conn = get_redis_connection('cart')
        if is_selected:
            redis_conn.sadd(f'selected_{user_id}', course_id)
        else:
            redis_conn.srem(f'selected_{user_id}', course_id)

        return Response({"msg":'勾选状态切换成功！'})


    def change_expire(self,request):

        user_id = request.user.id
        course_id = request.data.get('course_id')
        expire_id = request.data.get('expire_id')

        try:
            course = models.Course.objects.get(pk=course_id)
            # expire_id = 0 表示永久有效，永久有效数据没有保存在CourseExpire表中
            if expire_id > 0:

                expire_obj = models.CourseExpire.objects.filter(is_show=True,is_deleted=False,id=expire_id)
                if not expire_obj:
                    raise models.Course.DoesNotExist

        except models.Course.DoesNotExist:

            return Response({'msg': '商品或者有效期不存在！'}, status=status.HTTP_400_BAD_REQUEST)

        redis_conn = get_redis_connection('cart')
        redis_conn.hset('cart_%s' % user_id, course_id, expire_id)


        real_price = course.real_price(expire_id)

        return Response({'msg':'切换有有效期选项成功!','real_price':real_price})

    def delete_course(self,request):
        user_id = request.user.id
        print('user_id',user_id)
        #127.0.0.1:8001/?xx=oo
        course_id = request.query_params.get('course_id')



        try:
            course = models.Course.objects.get(pk=course_id)
        except models.Course.DoesNotExist:
            return Response({'msg':'删除课程不存在！'},status=status.HTTP_400_BAD_REQUEST)

        print('xxxxxxxxxxxxxx')
        redis_conn = get_redis_connection('cart')
        pipe = redis_conn.pipeline()
        pipe.multi()
        pipe.hdel("cart_%s" % user_id, course_id)
        pipe.srem("selected_%s" % user_id,course_id)

        pipe.execute()

        return Response({'msg':'删除商品成功'})


    def get_selected_course(self,request):
        """获取购物车中勾选的课程"""

        user_id = request.user.id
        # user_id = 1
        redis_conn = get_redis_connection('cart')

        cart_data_dict = redis_conn.hgetall("cart_%s" % user_id)
        selected_course_data = redis_conn.smembers("selected_%s" % user_id)

        data = []  #存放勾选中的课程相关数据
        total_price = 0
        real_total_price = 0
        for course_id_bytes, expire_bytes in cart_data_dict.items():

            course_id = int(course_id_bytes.decode())
            expire_id = int(expire_bytes.decode())
            if course_id_bytes in selected_course_data:
                try:
                    course_obj = models.Course.objects.get(pk=course_id)
                except:
                    continue


                expire_text = '永久有效'


                try:
                    if expire_id > 0:
                        expire_obj = models.CourseExpire.objects.get(is_show=True, is_deleted=False, id=expire_id)

                        expire_text = expire_obj.expire_text

                except models.CourseExpire.DoesNotExist:

                    return Response({'msg': '有效期不存在！'}, status=status.HTTP_400_BAD_REQUEST)


                real_price = course_obj.real_price(expire_id)

                data.append({
                    'id': course_obj.id,
                    'course_img': contants.SERVER_HOST + course_obj.course_img.url,
                    'name': course_obj.name,
                    # 'origin_price': course_obj.price,
                    'real_price': course_obj.real_price(expire_id),
                    'expire_text': expire_text,
                    'discount_name':course_obj.discount_name,

                    'origin_price':course_obj.price,

                })

                total_price += float(course_obj.price)
                real_total_price += float(real_price)

        return Response({"select_course_list": data, "total_price": total_price,'real_total_price':real_total_price})














