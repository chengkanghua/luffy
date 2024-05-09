from django.urls import path
from . import views

urlpatterns = [
    path(r'students/',views.StudentModelViewSet.as_view()),

]
