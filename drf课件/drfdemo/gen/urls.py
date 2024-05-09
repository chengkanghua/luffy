from django.urls import path,re_path

from . import views
# urlpatterns = [
#     # path(r'students/',views.StudentsGenericAPIView.as_view()),
#     # re_path(r'students/(?P<pk>\d+)/',views.StudentGenericAPIView.as_view()),
#
#     path(r'students/', views.StudentGenericViewSet.as_view({"get": "list", "post": "create"})),
#     re_path(r'students/(?P<pk>\d+)/', views.StudentGenericViewSet.as_view({"get": "retrieve","put":"update","delete":"destroy"})),
# ]

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'router_stu', views.StudentGenericViewSet,basename="student")

urlpatterns = []
urlpatterns += router.urls
# print(router.urls)
'''
[
<URLPattern '^router_stu/$' [name='student-list']>, 
<URLPattern '^router_stu\.(?P<format>[a-z0-9]+)/?$' [name='student-list']>, 
<URLPattern '^router_stu/(?P<pk>[^/.]+)/$' [name='student-detail']>, 
<URLPattern '^router_stu/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='student-detail']>, 
<URLPattern '' [name='api-root']>, 
<URLPattern '<drf_format_suffix:format>' [name='api-root']>]


'''


