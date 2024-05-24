from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from course.models import Course
from course import models
from rest_framework.response import Response
from rest_framework import status
from django_redis import get_redis_connection
from luffyapi.settings import constants
import logging
log = logging.getLogger("django")

class CartAPIView(ViewSet):
    """购物车"""
    #permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    def add(self,request):
        """添加商品到购物车中"""
        # 接受客户端提交参数[用户ID，课程ID，勾选状态，有效期选项]
        course_id = request.data.get("course_id")
        user_id = request.user.id
        #user_id = 1
        # 设置默认值
        selected = True
        expire = 0  #课程有效期，0表示永久有效，后面再改
        # 校验参数
        try:
            course = Course.objects.get(is_show=True, is_deleted=False, id=course_id)
        except Course.DoesNotExist:
            return Response({"message":"参数有误！课程不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        # 获取redis连接对象
        redis_conn = get_redis_connection("cart")
        # 保存数据到redis
        try:
            pipe = redis_conn.pipeline()
            pipe.multi()
            pipe.hset("cart_%s" % user_id, course_id, expire)
            pipe.sadd("selected_%s" % user_id, course_id)
            pipe.execute()

            # 查询购物车中商品总数
            course_len = redis_conn.hlen("cart_%s" % user_id)

        except:
            log.error("购物车数据存储错误！")
            return Response({"message": "参数有误！购物车添加商品失败！"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        # 返回结果[当前购物车中商品总数]
        return Response({"message":"购物车商品添加成功！","length": course_len})

    def list(self, request):
        """购物车中的商品列表"""
        user_id = request.user.id
        # 从redis中读取数据
        redis_conn = get_redis_connection("cart")
        cart_bytes_dict = redis_conn.hgetall("cart_%s" % user_id)
        selected_bytes_list = redis_conn.smembers("selected_%s" % user_id)
        # 使用循环从mysql中根据课程ID提取对应的商品信息[商品ID，商品封面图片，商品标题]
        data = []
        for course_id_bytes, expire_id_bytes in cart_bytes_dict.items():
            course_id = int(course_id_bytes.decode())
            expire_id = int(expire_id_bytes.decode())
            try:
                course = Course.objects.get(is_show=True, is_deleted=False, pk=course_id)
            except Course.DoesNotExist:
                continue
            data.append({
                "id": course.id,
                "name": course.name,
                "selected": True if course_id_bytes in selected_bytes_list else False,
                "course_img": constants.SERVER_IMAGE_DOMAIN + course.course_img.url,
                "expire_id": expire_id,
                "expire_list": course.expire_list,
                # "price": course.real_price,
                'origin_price': course.price,
                'real_price': course.real_price(expire_id),
                })
        return Response(data)

    def change_selected(self,request):
        """切换购物车商品的勾选状态"""
        user_id = request.user.id
        selected = request.data.get("selected")
        course_id = request.data.get("course_id")
        try:
            Course.objects.get(is_show=True, is_deleted=False, id=course_id)
        except Course.DoesNotExist:
            return Response({"message":"参数有误！当前商品课程不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        redis_conn = get_redis_connection("cart")
        #  true就添加 否则就删除
        if selected:
            redis_conn.sadd("selected_%s" % user_id, course_id)
        else:
            redis_conn.srem("selected_%s" % user_id, course_id)
        return Response({"message":"切换勾选状态成功！"})

    def all_selected(self,request):
        """购物车全部选中"""
        user_id = request.user.id
        status = request.data.get("status")
        redis_conn = get_redis_connection("cart")

        # 1 redis 查询当前用户的购物车的商品 只要id
        user_id = str(user_id)
        ret = redis_conn.hgetall("cart_%s" % user_id)
        # data = {key.decode(): value.decode() for (key, value) in ret.items()}
        data = [key.decode() for key in ret.keys()]
        if status:
            for course_id in data:
                redis_conn.sadd("selected_%s" % user_id, course_id )
        else:
            for course_id in data:
                redis_conn.srem("selected_%s" % user_id, course_id )
        # 2    user_id_selected:{1,2,3,4}

        return Response({"message": "ok"})

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
        return Response({'message':'切换有有效期选项成功!','real_price':real_price })

    def delete_cart(self,request):
        """从购物车中删除商品信息"""
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
        return Response({'message':'删除商品成功'})


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
                    'course_img': constants.SERVER_HOST + course_obj.course_img.url,
                    'name': course_obj.name,
                    'real_price': course_obj.real_price(expire_id),
                    'expire_text': expire_text,
                    'discount_name':course_obj.discount_name,
                    'origin_price':course_obj.price,

                })

                total_price += float(course_obj.price)
                real_total_price += float(real_price)

        return Response({"select_course_list": data, "total_price": total_price,'real_total_price':real_total_price})

























