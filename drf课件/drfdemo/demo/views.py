
from rest_framework.views import APIView
# Create your views here.
from students import models
from .serializers import StudentModelSerializer
from rest_framework.response import Response
from rest_framework import status

class StudentsAPIView(APIView):

    def get(self,request):
        """
        获取所有学生数据
        :param request:
        :return:
        """
        """
            简单总结：
                1 获取一个数据，传instance参数
                    获取多条数据，传instance,many=True参数
                2 更新数据，传instance和data参数
                    部分字段更新，可以增加partial=True参数
                3 添加数据，传data参数
                4 删除数据，不需要使用序列化器
        """
        data_list = models.Student.objects.all()
        serializer = StudentModelSerializer(instance=data_list,many=True)

        return Response(serializer.data)

    def post(self,request):
        """
        添加学生信息
        :param requeset:
        :return:
        """
        data = request.data
        serializer = StudentModelSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()
        # 将添加的新的数据返回给客户端，可以使用我们的序列化组件先序列化一下
        serializer = StudentModelSerializer(instance=instance)

        return Response(serializer.data,status=status.HTTP_201_CREATED)

class StudentAPIView(APIView):

    def get(self,request,pk):
        """获取单条数据"""
        instance = models.Student.objects.get(pk=pk)
        serializer = StudentModelSerializer(instance=instance)
        return Response(serializer.data)
    def put(self,request,pk):
        """更新学生信息"""
        #由于更新操作，我们需要找到被更新的是哪条记录，所以需要客户端给我们传一个id过来，并且以后我们会用到获取一条数据，删除一条数据，都需要用到一个id值，所以我们把上面的get和post方法写成一个类，更新、获取单条数据和删除数据我们再单独写一个类
        data = request.data
        student = models.Student.objects.get(id=pk)

        #可能提交过来的是部分数据，所以加上一个partial=True参数
        serializer = StudentModelSerializer(instance=student,data=data,partial=True)

        serializer.is_valid(raise_exception=True)

        instance = serializer.save()
        # 将修改后的数据返回给客户端
        serializer = StudentModelSerializer(instance=instance)

        return Response(serializer.data)


    def delete(self,request,pk):
        """删除一条数据,用不到我们的序列化器"""

        ret = models.Student.objects.get(id=pk).delete()

        return Response(None,status=status.HTTP_204_NO_CONTENT)
