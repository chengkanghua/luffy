from django.db import models
from django.contrib.auth.models import AbstractUser
from luffyapi.utils.model import BaseModel


# Create your models here.
class User(AbstractUser):
    """用户模型类"""
    mobile = models.CharField(max_length=15, unique=True, verbose_name='手机号码')
    avatar = models.ImageField(upload_to='avatar', verbose_name='用户头像', null=True, blank=True)
    wechat = models.CharField(max_length=60, null=True, blank=True)
    credit = models.IntegerField(default=0, blank=True, verbose_name="贝里")

    class Meta:
        db_table = 'ly_user'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class Credit(BaseModel):
    """积分流水"""
    OPERA_OPION = (
        (1, "赚取"),
        (2, "消费"),
    )
    user = models.ForeignKey("User", related_name="user_credit", on_delete=models.CASCADE, verbose_name="用户")
    opera = models.SmallIntegerField(choices=OPERA_OPION, verbose_name="操作类型")  # 赚取
    number = models.SmallIntegerField(default=0, verbose_name="积分数值")  # 50

    class Meta:
        db_table = 'ly_credit'
        verbose_name = '积分流水'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s %s %s 贝壳" % (self.user.username, self.OPERA_OPION[self.opera][1], self.number)


from course.models import Course


class UserCourse(BaseModel):
    """用户的课程购买记录"""
    pay_choices = (
        (1, '用户购买'),
        (2, '免费活动'),
        (3, '活动赠品'),
        (4, '系统赠送'),
    )
    user = models.ForeignKey(User, related_name='user_courses', on_delete=models.DO_NOTHING, verbose_name="用户")
    course = models.ForeignKey(Course, related_name='course_users', on_delete=models.DO_NOTHING, verbose_name="课程")
    trade_no = models.CharField(max_length=128, null=True, blank=True, verbose_name="支付平台的流水号",
                                help_text="将来依靠流水号到支付平台查账单")
    buy_type = models.SmallIntegerField(choices=pay_choices, default=1, verbose_name="购买方式")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="购买时间")
    out_time = models.DateTimeField(null=True, blank=True, verbose_name="过期时间")

    class Meta:
        db_table = 'ly_user_course'
        verbose_name = '课程购买记录'
        verbose_name_plural = verbose_name
