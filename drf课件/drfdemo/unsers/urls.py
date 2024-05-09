from django.urls import path
from unsers import views


urlpatterns = [
    path('students/',views.StudentView.as_view()),
]