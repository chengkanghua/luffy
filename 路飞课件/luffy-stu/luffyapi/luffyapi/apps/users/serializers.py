
import re

from .models import User
from rest_framework import serializers
from .utils import get_user_by_account
from rest_framework_jwt.settings import api_settings

from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from order.models import Order

class UserModelSerializer(serializers.ModelSerializer):
    """
    注册用户
    需要数据：手机号，密码，验证码
    """
    sms_code = serializers.CharField(min_length=4,max_length=6,required=True, help_text='短信验证码', write_only=True)
    token = serializers.CharField(max_length=1024,read_only=True,help_text='token认证字符串')
    # {id,username,token}

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'password', 'sms_code', 'token']
        extra_kwargs = {
            'id':{
                'read_only':True,
            },
            'username': {
                'read_only': True,
            },
            'password':{
                'write_only':True,
            },
            'mobile':{
                'write_only':True,
            }

        }

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        sms_code = attrs.get('sms_code')
        password = attrs.get('password')

        #校验一下手机号的格式
        if not re.match(r"^1[3-9]\d{9}$",mobile):
            raise serializers.ValidationError('对不起，您的手机号格式有误！')
        user = get_user_by_account(mobile)
        if user is not None:
            raise serializers.ValidationError('sorry，该手机号已经被注册过了')

        #todo 验证短信验证码是否正确
        redis_conn = get_redis_connection('sms_code')
        redis_sms_code = redis_conn.get('sms_%s' % mobile).decode()
        print(sms_code,type(sms_code))
        print(redis_sms_code,type(redis_sms_code))
        if sms_code != redis_sms_code:
            raise serializers.ValidationError('验证码输入有误!')
        return attrs

    def create(self, validated_data):
        validated_data.pop('sms_code')
        raw_password = validated_data.get('password')
        hash_password = make_password(raw_password)
        mobile = validated_data.get('mobile')
        user = User.objects.create(
            mobile=mobile,
            password=hash_password,
            username=mobile,
        )

        # 手动生成jwt
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user.token = token

        return user


class UserOrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','order_number','order_status','pay_time','course_list']





