from django.http import JsonResponse
from django.views import View
from msers.serializers import StudentModelSerializer
from students import models

# Create your views here.

class StudentModelViewSet(View):
    def get(self,request):
        data_list = models.Student.objects.all()
        serializer = StudentModelSerializer(instance=data_list,many=True)

        return JsonResponse(serializer.data,safe=False)

    def post(self,request):

        data = request.POST
        serializers = StudentModelSerializer(data=data)  # 这个使用save 方法是调用create

        # serializers = StudentModelSerializer(instance=instance,data=data)  # 这个使用save 方法是调用update

        status = serializers.is_valid(raise_exception=True)
        # print(status)
        # print(serializers.validated_data)
        student = serializers.save()  #上面使用的ModelSerializer，所以不需要我们自己写create方法了
        print(student)
        return JsonResponse({'msg':'henhao'})