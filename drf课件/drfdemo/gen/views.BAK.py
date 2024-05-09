from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin

from students.models import Student
from .serializers import StudentModelSerializer, StudentModel2Serializer
from rest_framework.response import Response

class StudentsGenericAPIView(CreateModelMixin,ListModelMixin,GenericAPIView):
    # 本次视图类中要操作的数据[必填]
    queryset = Student.objects.all() #基本上是固定的，查询就这么写
    # 本次视图类中要调用的默认序列化器[选填]
    serializer_class = StudentModelSerializer

    def get(self, request):
        """获取所有学生信息"""
        # serializer = self.get_serializer(instance=self.get_queryset(), many=True)
        #
        # return Response(serializer.data)
        return self.list(request)

    def post(self,request):
        """添加学生信息"""
        # data = request.data
        #
        # serializer = self.get_serializer(data=data)
        #
        # serializer.is_valid(raise_exception=True)
        #
        # instance = serializer.save()
        #
        # serializer = self.get_serializer(instance=instance)
        #
        # return Response(serializer.data)
        return self.create(request)

class StudentGenericAPIView(DestroyModelMixin,UpdateModelMixin,RetrieveModelMixin,GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    #一个视图中使用多个序列化类的方法，目前的例子是：get请求获取数据时，我们只给他两个字段数据，其他方法时我们给他所有字段数据，定义了这个get_serializer_class方法之后(其实是对父类的方法进行了重写)，其实上面的serializer_class就可以不同写了
    def get_serializer_class(self):
        """重写获取序列化器类的方法"""
        if self.request.method == "GET":
            return StudentModel2Serializer
        else:
            return StudentModelSerializer

    #在使用GenericAPIView实现获取操作单个数据时，我们试图方法中的参数变量pk最好是pk名，别叫id什么的，不然还需要进行一些其他的配置，比较麻烦一些了，简单看一下源码就知道了
    def get(self,request,pk):
        """获取一条数据"""
        # serializer = self.get_serializer(instance=self.get_object())
        #
        # return Response(serializer.data)
        return self.retrieve(request,pk)

    def put(self,request,pk):

        # data = request.data
        #
        # serializer = self.get_serializer(instance=self.get_object(),data=data)
        #
        # serializer.is_valid(raise_exception=True)
        #
        # serializer.save()
        #
        # serializer = self.get_serializer(instance=self.get_object())
        #
        # return Response(serializer.data)

        return self.update(request,pk)

    def delete(self,request,pk):
        '''删除一条数据'''
        return self.destroy(request,pk)