from django.urls import path
from . import views
urlpatterns = [
    path(r'students/',views.StudentAPIView.as_view()),

]