
from django.urls import path, re_path
from . import views
urlpatterns = [
    path(r'',views.CarTAPIView.as_view({'post':'add','get':'cart_list','patch': 'change_course_selected','put':'change_expire','delete':'delete_course'})) ,

    path(r'order/',views.CarTAPIView.as_view({'get':'get_selected_course'})) ,



]

