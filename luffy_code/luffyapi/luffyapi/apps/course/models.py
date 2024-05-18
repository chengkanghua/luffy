from django.db import models
from luffyapi.utils.model import BaseModel


# Create your models here.

class Teacher(BaseModel):
    """讲师、导师表"""
    role_choices = (
        (0, '讲师'),
        (1, '导师'),
        (2, '班主任'),
    )
    name = models.CharField(max_length=32, verbose_name="讲师title")
    role = models.SmallIntegerField(choices=role_choices, default=0, verbose_name="讲师身份")
    title = models.CharField(max_length=64, verbose_name="职位、职称")
    signature = models.CharField(max_length=255, verbose_name="导师签名", help_text="导师签名", blank=True, null=True)
    image = models.ImageField(upload_to="Teacher", null=True, verbose_name="讲师封面")
    brief = models.TextField(max_length=1024, verbose_name="讲师描述")

    class Meta:
        db_table = "ly_teacher"
        verbose_name = "讲师导师"
        verbose_name_plural = "讲师导师"

    def __str__(self):
        return "%s" % self.name

class CourseChapter(BaseModel):
    """课程章节"""
    course = models.ForeignKey("Course", related_name='coursechapters', on_delete=models.CASCADE, verbose_name="课程名称")
    chapter = models.SmallIntegerField(verbose_name="第几章", default=1)
    name = models.CharField(max_length=128, verbose_name="章节标题")
    summary = models.TextField(verbose_name="章节介绍", blank=True, null=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)

    class Meta:
        db_table = "ly_course_chapter"
        verbose_name = "课程章节"
        verbose_name_plural = "课程章节"

    def __str__(self):
        return "%s:(第%s章)%s" % (self.course, self.chapter, self.name)


class CourseLesson(BaseModel):
    """课程课时"""
    section_type_choices = (
        (0, '文档'),
        (1, '练习'),
        (2, '视频')
    )
    chapter = models.ForeignKey("CourseChapter", related_name='coursesections', on_delete=models.CASCADE,
                                verbose_name="课程章节")
    name = models.CharField(max_length=128, verbose_name="课时标题")
    # orders = models.PositiveSmallIntegerField(verbose_name="课时排序") #在basemodel里面已经有了排序了
    section_type = models.SmallIntegerField(default=2, choices=section_type_choices, verbose_name="课时种类")
    section_link = models.CharField(max_length=255, blank=True, null=True, verbose_name="课时链接",
                                    help_text="若是video，填vid,若是文档，填link")
    duration = models.CharField(verbose_name="视频时长", blank=True, null=True,
                                max_length=32)  # 仅在前端展示使用，所以直接让上传视频的用户直接填写时长进来就可以了。
    pub_date = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    free_trail = models.BooleanField(verbose_name="是否可试看", default=False)
    course = models.ForeignKey('Course', related_name='course_lesson', verbose_name='课程', on_delete=models.CASCADE,
                               null=True, blank=True)
    is_show_list = models.BooleanField(verbose_name='是否推荐到课程列表', default=False)
    lesson = models.IntegerField(verbose_name="第几课时")


    class Meta:
        db_table = "ly_course_lesson"
        verbose_name = "课程课时"
        verbose_name_plural = "课程课时"


    def __str__(self):
        return "%s-%s" % (self.chapter, self.name)
        from django.db import models

class CourseCategory(BaseModel):
    """
    课程分类
    """
    name = models.CharField(max_length=64, unique=True, verbose_name="分类名称")

    class Meta:
        db_table = "ly_course_category"
        verbose_name = "课程分类"
        verbose_name_plural = "课程分类"

    def __str__(self):
        return "%s" % self.name


class Course(BaseModel):
    """
    专题课程
    """
    course_type = (
        (0, '付费'),
        (1, 'VIP专享'),
        (2, '学位课程')
    )
    level_choices = (
        (0, '初级'),
        (1, '中级'),
        (2, '高级'),
    )
    status_choices = (
        (0, '上线'),
        (1, '下线'),
        (2, '预上线'),
    )
    name = models.CharField(max_length=128, verbose_name="课程名称")
    course_img = models.ImageField(upload_to="course", max_length=255, verbose_name="封面图片", blank=True, null=True)

    # 费用类型字段是为了后期一些其他功能拓展用的，现在可以先不用，或者去掉它，目前我们项目用不到
    course_type = models.SmallIntegerField(choices=course_type, default=0, verbose_name="付费类型")
    # 这个字段是课程详情页里面展示的，并且详情介绍里面用户将来可能要上传一些图片之类的，所以我们会潜入富文本编辑器，让用户填写数据的时候可以上传图片啊、写标题啊、css、html等等内容
    brief = models.TextField(max_length=2048, verbose_name="详情介绍", null=True, blank=True)

    level = models.SmallIntegerField(choices=level_choices, default=1, verbose_name="难度等级")
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)
    period = models.IntegerField(verbose_name="建议学习周期(day)", default=7)

    # 课件资料的存放路径
    attachment_path = models.FileField(max_length=128, verbose_name="课件路径", blank=True, null=True)
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="课程状态")
    course_category = models.ForeignKey("CourseCategory", on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name="课程分类")
    students = models.IntegerField(verbose_name="学习人数", default=0)
    lessons = models.IntegerField(verbose_name="总课时数量", default=0)

    # 总课时数量可能10个，但是目前之更新了3个，就跟小说、电视剧连载似的。
    pub_lessons = models.IntegerField(verbose_name="课时更新数量", default=0)

    # 课程原价
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程原价", default=0)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="授课老师")

    class Meta:
        db_table = "ly_course"
        verbose_name = "专题课程"
        verbose_name_plural = "专题课程"

    def __str__(self):
        return "%s" % self.name

    def lesson_list(self):
        """获取当前课程的前8个课时展示到列表中"""

        # 获取所有章节
        chapters_list = self.coursechapters.filter(is_deleted=False,is_show=True)
        lesson_list = []
        if chapters_list:
            for chapter in chapters_list:
                lessons = chapter.coursesections.filter(is_deleted=False,is_show=True)[:4]
                if lessons:
                    for lesson in lessons:
                        lesson_list.append({
                            "id":lesson.id,
                            "name":lesson.name,
                            "free_trail":lesson.free_trail
                        })

        return lesson_list[:4]


