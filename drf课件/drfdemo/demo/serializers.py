from rest_framework import serializers
from students.models import Student


class StudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__" # 表示操作模型中的所有字段
