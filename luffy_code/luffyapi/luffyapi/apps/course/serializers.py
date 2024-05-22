from rest_framework import serializers
from .models import CourseCategory, Course, Teacher
from . import models


class CourseCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ["id","name"]



class TeacherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ['id','name','role','image','brief','title','signature']


class CourseModelSerializer(serializers.ModelSerializer):
    """课程信息的序列化器"""
    # 序列化器嵌套
    teacher = TeacherModelSerializer()  # 老师 1 : 多课程

    # teacher = CourseTeacherModelSerializer(many=True) # 多对1
    class Meta:
        model = Course
        fields = ("id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "teacher","lesson_list",'discount_name','real_price')

class CourseDetailModelSerializer(serializers.ModelSerializer):
    """课程详情页的序列化器"""

    teacher = TeacherModelSerializer()

    class Meta:
        model = models.Course
        fields = ["id","name","course_img","students","lessons","pub_lessons","price","teacher","brief","level",'level_name','brief_html','course_video','discount_name','real_price','active_time']


class CourseLessonModelSerializer(serializers.ModelSerializer):
    """课时序列化器"""
    class Meta:
        model = models.CourseLesson
        fields = ['id','free_trail','name','lesson','duration']


class CourseChapterModelSerializer(serializers.ModelSerializer):
    """章节序列化器"""
    coursesections = CourseLessonModelSerializer(many=True)

    class Meta:
        model = models.CourseChapter
        fields = ['id','chapter','name','coursesections']










