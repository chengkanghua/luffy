from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin

from students.models import Student
from .serializers import StudentModelSerializer, StudentModel2Serializer
from rest_framework.response import Response

class StudentsGenericAPIView(CreateModelMixin,ListModelMixin,GenericAPIView):
    queryset = Student.objects.all() #基本上是固定的，查询就这么写
    serializer_class = StudentModelSerializer

    def get(self, request):
        """获取所有学生信息"""
        return self.list(request)

    def post(self,request):
        """添加学生信息"""
        return self.create(request)

class StudentGenericAPIView(DestroyModelMixin,UpdateModelMixin,RetrieveModelMixin,GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get_serializer_class(self):
        """重写获取序列化器类的方法"""
        if self.request.method == "GET":
            return StudentModel2Serializer
        else:
            return StudentModelSerializer

    def get(self,request,pk):
        """获取一条数据"""
        return self.retrieve(request,pk)

    def put(self,request,pk):
        '''修改一条数据'''
        return self.update(request,pk)

    def delete(self,request,pk):
        '''删除一条数据'''
        return self.destroy(request,pk)