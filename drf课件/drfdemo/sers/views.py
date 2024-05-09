
from django.views import View
from students.models import Student
from .serializers import StudentSerializer
from django.http.response import JsonResponse
# Create your views here.

class StudentView(View):
    """使用序列化器序列化转换单个模型数据"""
    def get(self,request):
        # 获取数据
        student_list = Student.objects.all()
        # 数据转换[序列化过程]
        serializer = StudentSerializer(instance=student_list, many=True)
        print(serializer.data)
        # 响应数据
        return JsonResponse(serializer.data,safe=False,json_dumps_params={'ensure_ascii':False})