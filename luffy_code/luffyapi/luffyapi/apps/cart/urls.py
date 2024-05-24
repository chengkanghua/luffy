from django.urls import path,re_path
from . import views



urlpatterns = [
    path(r"", views.CartAPIView.as_view({"post":"add","get":"list","patch":"change_selected","put":"change_expire","delete":"delete_cart"}) ),
    path(r"update/", views.CartAPIView.as_view({"put":"all_selected"}) ),
    path(r"order/", views.CartAPIView.as_view({"get":"get_selected_course"}) ),

]