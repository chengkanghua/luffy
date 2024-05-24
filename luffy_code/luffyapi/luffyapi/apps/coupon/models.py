from django.db import models
from luffyapi.utils.model import BaseModel
from users.models import User
from datetime import timedelta
# Create your models here.
class Coupon(BaseModel):
    """优惠券"""
    coupon_choices = (
        (0, '折扣优惠'),
        (1, '减免优惠')
    )
    name = models.CharField(max_length=32, verbose_name="优惠券标题")
    coupon_type = models.SmallIntegerField(choices=coupon_choices, default=0, verbose_name="优惠券类型")
    timer = models.IntegerField(verbose_name="优惠券有效期", default=7, help_text="默认当前优惠券7天有效，如果设置值为-1则表示当前优惠券永久有效")
    condition = models.IntegerField(blank=True, default=0, verbose_name="满足使用优惠券的价格条件，如果设置值为0,则表示没有任何条件")
    sale = models.TextField(verbose_name="优惠公式", help_text="""
        *号开头表示折扣价，例如*0.82表示八二折；<br>
        -号开头表示减免价,例如-10表示在总价基础上减免10元<br>    
        """)

    class Meta:
        db_table = "ly_coupon"
        verbose_name="优惠券"
        verbose_name_plural="优惠券"

    def __str__(self):
        return "%s" % (self.name)

class UserCoupon(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users", verbose_name="用户")
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="coupons", verbose_name="优惠券")
    start_time = models.DateTimeField(verbose_name="优惠策略的开始时间")
    is_use = models.BooleanField(default=False,verbose_name="优惠券是否使用过")

    class Meta:
        db_table = "ly_user_coupon"
        verbose_name = "用户的优惠券"
        verbose_name_plural = "用户的优惠券"

    def __str__(self):
        return "优惠券:%s,用户:%s" % (self.coupon.name, self.user.username)

    @property
    def end_time(self):
        """获取优惠券的过期时间"""
        # start_timestamp = self.start_time.timestamp()
        # use_time = self.coupon.timer * 24 * 60 * 60
        # end_timestamp = start_timestamp+use_time
        # return datetime.fromtimestamp(end_timestamp).strftime('%Y-%m-%d %H:%M:%S')

        start_time = self.start_time
        end_time = start_time + timedelta(days=self.coupon.timer)
        return end_time.strftime('%Y-%m-%d %H:%M:%S')