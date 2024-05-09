from rest_framework import serializers

def check_name(val):
    if '666' not in val:
        return val
    else:
        raise serializers.ValidationError("不能包含666")


class StudentSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=20,validators=[check_name,])
    age = serializers.IntegerField(max_value=150, min_value=0,required=True)
    sex = serializers.BooleanField(default=True)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)


    def validate_name(self,data):
        if(data=="老男孩666"):
            raise serializers.ValidationError("用户名不能是老男孩666")
        # 验证完成以后务必要返回字段值
        return data


    def validate(self,data):
        name = data.get("name")
        if(name == "python"):
            raise serializers.ValidationError("用户名不能是python")

        age = data.get("age")
        if(age==0):
            raise serializers.ValidationError("年龄不能是0")

        # 验证完成以后务必要返回data
        return data

        # 添加和更新代码
        # 序列化器中会提供了两个方法: create 和 update,方法名是固定的
    def create(self, validated_data):  # validated_data 参数,在序列化器调用时,会自动传递验证完成以后的数据
        student = Student.objects.create(
            name=self.validated_data.get("name"),
            age=self.validated_data.get("age"),
            sex=self.validated_data.get("sex"),
            description=serializer.validated_data.get("description")
        )

        return student

    def update(self, instance, validated_data):  # instance表示当前更新的记录对象
        """更新学生信息"""
        instance.name = validated_data.get("name")
        instance.sex = validated_data.get("sex")
        instance.age = validated_data.get("age")
        instance.description = validated_data.get("description")
        # 调用模型的save更新保存数据
        instance.save()

        return instance