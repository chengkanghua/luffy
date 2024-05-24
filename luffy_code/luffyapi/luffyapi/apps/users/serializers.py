from django_redis import get_redis_connection
from rest_framework import serializers
from .models import User
import re
from .utils import get_user_by_account
from django.contrib.auth.hashers import make_password
from rest_framework_jwt.settings import api_settings

import logging
log = logging.getLogger("django")

class UserModelSerializer(serializers.ModelSerializer):
    sms_code = serializers.CharField(min_length=4, max_length=6, required=True, write_only=True, help_text="短信验证码")
    token = serializers.CharField(max_length=1024, read_only=True, help_text="token认证字符串")
    class Meta:
        model = User
        #注册之后我们按说就不应该让他再登录了，也就是免登录，所以我们需要给它返回id，username和token
        fields = ["id","username", "mobile","password","sms_code","token"]
        extra_kwargs = {
            "id":{
                "read_only":True,
            },
            "username":{
                "read_only":True,
            },
            "password":{
                "write_only":True,
            },
            "mobile":{
                "write_only":True,
            }
        }

    def validate(self, attrs):
        mobile = attrs.get("mobile")
        sms_code = attrs.get("sms_code")
        password = attrs.get("password")

        # 验证手机号码的格式
        if not re.match(r"^1[3-9]\d{9}$", mobile):
           raise serializers.ValidationError("对不起，手机号格式有误！")

        # 验证手机短信
        try:
            redis = get_redis_connection("sms_code")
        except:
            log.error("redis连接失败！")
            raise serializers.ValidationError("redis服务器出错，请联系客服工作人员!")

        # 验证短信是否有效
        try:
            real_sms_code = redis.get("sms_%s" % mobile).decode()
        except:
            raise serializers.ValidationError("手机短信不存在或已过期！")

        # 验证短信是否正确
        if sms_code != real_sms_code:
            raise serializers.ValidationError("手机短信错误！")

        # 验证码手机号是否已经被注册过了
        ret = get_user_by_account(mobile)
        if ret is not None:
            raise serializers.ValidationError("对不起，手机号已经被注册过！")

        # 验证密码长度
        if len(password) < 6 or len(password) > 16:
            raise serializers.ValidationError("密码必须保持在6-16位字符长度之间!")

        return attrs

    def create(self, validated_data):
        """用户信息"""
        # 移除掉不需要的数据
        validated_data.pop("sms_code")
        # 对密码进行加密
        raw_password =  validated_data.get("password")
        hash_password = make_password(raw_password)
        # 对用户名设置一个默认值
        username = validated_data.get("mobile")
        # 调用序列化器提供的create方法
        try:
            user = User.objects.create(
                mobile=username,
                username=username,
                password=hash_password,
            )
        except:
            log.error("创建用户失败！mobile=%s" % username)
            raise serializers.ValidationError("注册用户失败！请联系客服工作人员！")

        # 注册成功以后，默认当前用户为登录状态，返回返回登录的jwt token值
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)

        return user

from order.models import Order
class UserOrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','order_number','order_status','pay_time','course_list']


