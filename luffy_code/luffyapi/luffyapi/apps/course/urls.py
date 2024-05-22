from django.urls import path, re_path
from . import views


urlpatterns = [
    path(r'category/', views.CourseCategoryListAPIView.as_view() ),
    path(r'list/', views.CourseListAPIView.as_view()),
    re_path(r'detail/(?P<pk>\d+)/', views.CourseRetrieveAPIView.as_view()),
    path("chapter/", views.CourseChapterAPIView.as_view()),
]
