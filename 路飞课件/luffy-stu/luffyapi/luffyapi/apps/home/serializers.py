
from rest_framework import serializers
from . import models
class BannerModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Banner
        fields = ['link','image_url']


class NavModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Nav
        fields = ['id','title','link','is_site']




