from django.http import JsonResponse
from django.views import View
from .serializers import StudentSerializer
from students.models import Student


class StudentView(View):
    def post(self, request):
        """添加一个学生"""
        # 接受参数
        # content-type:'application/json' #django默认解析不了这种数据格式
        # urlencoded #在postman修改成这种格式再发送
        post_data = request.POST
        print(post_data)
        data = {
            "name": post_data.get('name'),
            "age": post_data.get('age'),
            "sex": post_data.get('sex'),
            "description": post_data.get('description'),
        }
        # 调用序列化器进行反序列化验证和转换
        serializer = StudentSerializer(data=data)
        # serializer.errors  # 查看错误信息

        # 当验证失败时,可以直接通过声明 raise_exception=True 让django直接跑出异常,那么验证出错之后，直接就再这里报错，程序中断了就
        # result = serializer.is_valid(raise_exception=True)
        # print("验证结果:%s" % result)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return JsonResponse(serializer.errors)  # 返回校验的错误信息


        # 获取通过验证后的数据
        print(serializer.validated_data)  # form -- clean_data
        # 保存数据
        student = Student.objects.create(
            name=serializer.validated_data.get("name"),
            age=serializer.validated_data.get("age"),
            sex=serializer.validated_data.get("sex"),
            description=serializer.validated_data.get("description")
        )

        print(student)
        # 返回响应结果给客户端
        # alt + enter，可以实现快速导包
        return JsonResponse({"message": "ok"})

    def put(self,request):
        """更新学生信息"""
        # 接受参数
        data = {
            "id":9,
            "name":"abc",
            "age":18,
            "sex":1,
            "description":"测试",
        }
        # 获取要修改的数据
        instance = Student.objects.get(pk=data.get("id"))
        # 调用序列化器
        serializer = StudentSerializer(instance=instance,data=data)
        # 验证
        serializer.is_valid(raise_exception=True)
        # 转换成模型数据
        student = serializer.save()

        return JsonResponse({"message": "ok"})


