from django.db import models
from luffyapi.utils.models import BaseModel
from users.models import User
from course.models import Course,CourseExpire
from luffyapi.settings import contants

class Order(BaseModel):
    """订单模型"""
    status_choices = (
        (0, '未支付'),
        (1, '已支付'),
        (2, '已取消'),
        (3, '超时取消'),
    )
    pay_choices = (
        (0, '支付宝'),
        (1, '微信支付'),
    )
    order_title = models.CharField(max_length=150,verbose_name="订单标题")
    total_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="订单总价", default=0)
    real_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="实付金额", default=0)
    order_number = models.CharField(max_length=64,verbose_name="订单号")
    order_status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="订单状态")
    pay_type = models.SmallIntegerField(choices=pay_choices, default=1, verbose_name="支付方式")
    credit = models.IntegerField(default=0, verbose_name="使用的积分数量")
    coupon = models.IntegerField(null=True, verbose_name="用户优惠券ID")
    order_desc = models.TextField(max_length=500, verbose_name="订单描述",null=True,blank=True)
    pay_time = models.DateTimeField(null=True, verbose_name="支付时间")
    user = models.ForeignKey(User, related_name='user_orders', on_delete=models.DO_NOTHING,verbose_name="下单用户")

    class Meta:
        db_table="ly_order"
        verbose_name= "订单记录"
        verbose_name_plural= "订单记录"

    def __str__(self):
        return "%s,总价: %s,实付: %s" % (self.order_title, self.total_price, self.real_price)

    def course_list(self):
        order_details = self.order_courses.all()
        data = []
        for order_detail in order_details:
            course_obj = order_detail.course
            expire_id = order_detail.expire
            if expire_id > 0:
                expire_text = CourseExpire.objects.get(pk=expire_id).expire_text
            else:
                expire_text = '永久有效'

            data.append({
                'course_img':contants.SERVER_HOST + course_obj.course_img.url,
                'course_name':course_obj.name,
                'expire_text':expire_text,
                'discount_name':course_obj.discount_name,
                'origin_price':order_detail.price,
                'real_price':order_detail.real_price,

            })
            print(data)
        return data

class OrderDetail(BaseModel):
    """
    订单详情
    """
    order = models.ForeignKey(Order, related_name='order_courses', on_delete=models.CASCADE, verbose_name="订单ID")
    course = models.ForeignKey(Course, related_name='course_orders', on_delete=models.CASCADE, verbose_name="课程ID")
    expire = models.IntegerField(default='0', verbose_name="有效期周期",help_text="0表示永久有效")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程原价")
    real_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程实价")
    discount_name = models.CharField(max_length=120,default="",verbose_name="优惠类型")

    class Meta:
        db_table="ly_order_detail"
        verbose_name= "订单详情"
        verbose_name_plural= "订单详情"

    def __str__(self):
        return "%s" % (self.course.name)