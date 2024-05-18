
from rest_framework.generics import ListAPIView
from .models import CourseCategory,Course
from .serializers import CourseCategoryModelSerializer
class CourseCategoryListAPIView(ListAPIView):
    queryset = CourseCategory.objects.filter(is_show=True,is_deleted=False).order_by("orders")
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


