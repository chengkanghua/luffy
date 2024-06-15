

from django.urls import path,re_path
from . import views
urlpatterns = [
    path(r'category/',views.CourseCategoryAPIView.as_view()),
    path(r'list/',views.CourseListAPIView.as_view()),

    re_path(r'detail/(?P<pk>\d+)/',views.CourseRetrieveAPIView.as_view()),

    path(r'chapter/',views.CourseChapterAPIView.as_view()),

    path(r'polyv/',views.PolyvAPIView.as_view()),

]
