from django.urls import path,re_path

from . import views
urlpatterns = [
    path(r'students/',views.StudentsAPIView.as_view()),
    re_path(r'students/(?P<pk>\d+)/',views.StudentAPIView.as_view()),
]