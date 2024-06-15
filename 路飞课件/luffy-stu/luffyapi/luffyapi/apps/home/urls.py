from django.urls import path
from . import views
urlpatterns = [
    path(r'banner/',views.BannerAPIView.as_view()),
    path(r'nav/',views.NavAPIView.as_view()),

]