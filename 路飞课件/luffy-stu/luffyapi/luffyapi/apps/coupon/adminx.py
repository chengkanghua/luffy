import xadmin
from .models import Coupon
class CouponModelAdmin(object):
    """优惠券模型管理类"""
    list_display = ["name","coupon_type","timer"]
xadmin.site.register(Coupon, CouponModelAdmin)


from .models import UserCoupon
class UserCouponModelAdmin(object):
    """我的优惠券模型管理类"""
    list_display = ["id","user","coupon","start_time","is_use"]

xadmin.site.register(UserCoupon, UserCouponModelAdmin)