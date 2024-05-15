from rest_framework import serializers
from .models import Banner


class BannerModelSerializer(serializers.ModelSerializer):
    '''轮播广告序列化器'''

    # 模型序列化字段声明
    class Meta:
        model = Banner
        fields = ["image_url", "link"]
