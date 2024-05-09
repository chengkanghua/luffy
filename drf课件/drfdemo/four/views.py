from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from four.utils.auth import APIAuth



class AuthAPIView(APIView):
    # authentication_classes = [APIAuth,]
    # permission_classes = [IsAuthenticated,]
    def get(self,request):
        print('>>>>',request.user)  #AnonymousUser  匿名用户，假用户
        print('>>>>',request.auth)  #AnonymousUser  匿名用户，假用户
        #>>>> root
        return Response({'msg':'hello'})



from rest_framework.pagination import PageNumberPagination
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2  # 每页显示量
    # http://127.0.0.1:8000/four/student/?page=1&page_size=10
    page_size_query_param = 'page_size'  # 提供客户端自行控制每页显示多少
    #page_query_param = "pp"              # 默认page 修改页面查询关键字 http://127.0.0.1:8000/four/student/?pp=3
    max_page_size = 10000


from .utils.permissions import IsXiaoMingPermission
from students.models import Student
from .serializers import StudentModelSerializer
from rest_framework.throttling import UserRateThrottle
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    # permission_classes = [IsXiaoMingPermission]
    # throttle_classes = (UserRateThrottle,)
    filter_fields = ('age', 'sex')
    filter_backends = [OrderingFilter,DjangoFilterBackend]
    ordering_fields = ('id', 'age')
    pagination_class = LargeResultsSetPagination




from rest_framework.views import APIView
from students.models import Student
from .serializers import StudentModelSerializer

class APIErrorxx(Exception):
    pass

class StudentAPI(APIView):
    def get(self,request,pk):
        try:
            instance = Student.objects.get(pk=pk)
        # except Student.DoesNotExist:
        except Exception:
            raise APIErrorxx('查询有误')
            return Response({'message':'访问的商品已经下架~'})

        serializer = StudentModelSerializer(instance=instance)
        return Response(serializer.data)




