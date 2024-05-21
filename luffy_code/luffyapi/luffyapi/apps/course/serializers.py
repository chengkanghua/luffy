from rest_framework import serializers
from .models import CourseCategory, Course, Teacher
class CourseCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ["id","name"]


class CourseTeacherModelSerializer(serializers.ModelSerializer):
    """课程所属老师的序列化器"""

    class Meta:
        model = Teacher
        fields = ("name", "title", "signature")


class CourseModelSerializer(serializers.ModelSerializer):
    """课程信息的序列化器"""
    # 序列化器嵌套
    teacher = CourseTeacherModelSerializer()  # 老师 1 : 多课程

    # teacher = CourseTeacherModelSerializer(many=True) # 多对1
    class Meta:
        model = Course
        fields = ("id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "teacher","lesson_list")












