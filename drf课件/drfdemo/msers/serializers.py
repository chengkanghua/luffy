from rest_framework import serializers
from students.models import Student


class StudentModelSerializer(serializers.ModelSerializer):
    # 字段声明
    # r_password = serializers.CharField() #额外字段  确认密码

    # 如果模型类序列化器,必须声明本次调用是哪个模型,模型里面的哪些字段
    class Meta:
        model = Student
        fields = ["id", "name", "age", "description", "sex"]
        # fields = "__all__" # 表示操作模型中的所有字段
        # 添加额外的验证选项
        # exclude = ['id', ]  # 排除字段
        extra_kwargs = {
            "sex": {"write_only": True, },
            "id": {"read_only": True, }
        }
