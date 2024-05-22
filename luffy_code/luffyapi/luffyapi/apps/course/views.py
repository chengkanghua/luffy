from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.conf import settings
from .models import CourseCategory,Course
from .serializers import CourseCategoryModelSerializer
from . import models
from luffyapi.libs.polyv import PolyvPlayer


class CourseCategoryListAPIView(ListAPIView):
    queryset = models.CourseCategory.objects.filter(is_show=True,is_deleted=False).order_by('orders','-id')
    serializer_class = CourseCategoryModelSerializer


from .serializers import CourseModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .paginations import CustomPageNumberPagination

class CourseListAPIView(ListAPIView):
    queryset = Course.objects.filter(is_deleted=False, is_show=True).order_by("orders")
    serializer_class = CourseModelSerializer
    # 设置价格排序
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filter_fields = ('course_category',)
    ordering_fields = ('id', 'students', 'price')
    # 指定分页器
    pagination_class = CustomPageNumberPagination


from rest_framework.generics import RetrieveAPIView
from .serializers import CourseDetailModelSerializer
class CourseRetrieveAPIView(RetrieveAPIView):
    queryset = models.Course.objects.filter(is_show=True,is_deleted=False).order_by('orders')
    serializer_class = CourseDetailModelSerializer


from .serializers import CourseChapterModelSerializer
class CourseChapterAPIView(ListAPIView):
    queryset = models.CourseChapter.objects.filter(is_deleted=False,is_show=True).order_by('orders','id')
    serializer_class = CourseChapterModelSerializer
    filter_backends = [DjangoFilterBackend,]
    filter_fields = ['course',]
    #127.0.0.1:8001/?course=2


class PolyvAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self,request):

        #userId,secretkey,tokenUrl
        userId = settings.POLYV_CONFIG['userId']
        secretkey = settings.POLYV_CONFIG['secretkey']
        tokenUrl = settings.POLYV_CONFIG['tokenUrl']

        polyv_obj = PolyvPlayer(userId, secretkey, tokenUrl)
        # videoId, viewerIp, viewerId=None, viewerName='', extraParams='HTML5'
        # vid = 'e3a65556c5de813fdaeee5b94da6868c_e'
        # request.GET
        vid = request.query_params.get('vid')
        viewerIp = request.META.get('REMOTE_ADDR')

        viewerId = request.user.id
        # viewerId = 1
        # viewerName = request.user.username
        # viewerName = 'root'
        viewerName = request.user.username
        ret = polyv_obj.get_video_token(vid, viewerIp, viewerId, viewerName)
        '''
        {
            "token": "edbbbfa2-3e07-42ea-b22b-e7f324bdcf9e-i1",
            "userId": "e3a65556c5",
            "appId": null,
            "videoId": "e3a65556c5de813fdaeee5b94da6868c_e",
            "viewerIp": "127.0.0.1",
            "viewerId": "1",
            "viewerName": "root",
            "extraParams": "HTML5",
            "ttl": 600000,
            "createdTime": 1592191516935,
            "expiredTime": 1592192116935,
            "iswxa": 0,
            "disposable": false
        }
        '''

        # return Response(ret)
        return HttpResponse(ret.get('token'))






