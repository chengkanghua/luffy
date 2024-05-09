# from rest_framework import routers
# from . import views
#
#
# router = routers.DefaultRouter()
# router.register(r'AuthAPIView', views.AuthAPIView,basename='AuthAPIView')
#
# urlpatterns = []
# urlpatterns += router.urls


from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'auth/',views.AuthAPIView.as_view()),
    path(r'student/',views.StudentViewSet.as_view({"get": "list", "post": "create"})),
    re_path(r'exce/(?P<pk>\d+)/',views.StudentAPI.as_view()),
]