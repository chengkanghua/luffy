from rest_framework import serializers
from .models import Coupon, UserCoupon
class CouponModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ("name","coupon_type","timer","condition","sale")


class UserCouponModelSerializer(serializers.ModelSerializer):
    coupon = CouponModelSerializer()
    class Meta:
        model = UserCoupon
        fields = ("id","start_time","coupon","end_time")