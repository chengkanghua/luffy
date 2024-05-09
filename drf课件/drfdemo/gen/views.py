from rest_framework.generics import ListAPIView, CreateAPIView,RetrieveAPIView,DestroyAPIView,UpdateAPIView

from students.models import Student
from .serializers import StudentModelSerializer, StudentModel2Serializer
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin


# class StudentsGenericAPIView(ListAPIView,CreateAPIView):
#     queryset = Student.objects.all() #基本上是固定的，查询就这么写
#     serializer_class = StudentModelSerializer
#
#
#
# class StudentGenericAPIView(RetrieveAPIView,DestroyAPIView,UpdateAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentModelSerializer
#     def get_serializer_class(self):
#         """重写获取序列化器类的方法"""
#         if self.request.method == "GET":
#             return StudentModel2Serializer
#         else:
#             return StudentModelSerializer


from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from students.models import Student
from .serializers import StudentModelSerializer

class StudentGenericViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    # methods 设置当前方法允许哪些http请求访问当前视图方法
    # detail 设置当前视图方法是否是操作一个数据
    # detail为True，表示路径名格式应该为 router_stu/{pk}/login/
    # http://127.0.0.1:8000/gen/router_stu/1/login/
    @action(methods=['get'],detail=True)
    def login(self,request,pk):
        """学生登录功能"""
        print(self.action)
        return Response({"message":"登录成功"})
    # detail为False 表示路径名格式应该为 router_stu/login2/
    # http://127.0.0.1:8000/gen/router_stu/login2/
    @action(methods=['get'],detail=False)
    def login2(self,request):
        """学生登录功能"""
        print(self.action)
        return Response({"message":"登录成功"})