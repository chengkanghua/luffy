from rest_framework import serializers
from students import models

# 创建序列化器类，回头会在试图中被调用
class StudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = "__all__"