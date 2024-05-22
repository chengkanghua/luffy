from datetime import datetime

from django.db import models
from luffyapi.utils.model import BaseModel
from luffyapi.settings import constants

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

from ckeditor_uploader.fields import RichTextUploadingField
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
    course_video = models.FileField(upload_to='video', null=True, blank=True, verbose_name='封面视频')

    # 费用类型字段是为了后期一些其他功能拓展用的，现在可以先不用，或者去掉它，目前我们项目用不到
    course_type = models.SmallIntegerField(choices=course_type, default=0, verbose_name="付费类型")
    # 这个字段是课程详情页里面展示的，并且详情介绍里面用户将来可能要上传一些图片之类的，所以我们会潜入富文本编辑器，让用户填写数据的时候可以上传图片啊、写标题啊、css、html等等内容
    # brief = models.TextField(max_length=2048, verbose_name="详情介绍", null=True, blank=True)
    brief = RichTextUploadingField(max_length=2048, verbose_name="课程概述", null=True, blank=True)

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
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程原价", default=0,help_text='如果填写的价格为0，那么表示当前课程在购买的时候，没有永久有效的期限。')
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

    @property
    def level_name(self):
        return self.level_choices[self.level][1]

    def brief_html(self):
        host = constants.SERVER_HOST
        html = self.brief.replace('src="/media',f'src="{host}/media')
        return html

    def active_list(self):
        active_lists = self.activeprices.filter(is_show=True, is_deleted=False, active__start_time__lte=datetime.now(),active__end_time__gte=datetime.now())
        # 一个商品可能多个活动策略
        return active_lists

    @property
    def discount_name(self):
        name = ''
        active_lists = self.active_list()
        # print(active_lists)
        if len(active_lists) > 0:
            active_obj = active_lists[0]  # 只取第一条
            name = active_obj.discount.discount_type.name
        return name

    # @property
    # def real_price(self):
    #     return self.price

    # @property
    def real_price(self,expire_id=0):
        """真实价格计算"""
        price = float(self.price)  #原价
        try:
            if expire_id > 0:
                expire_obj = CourseExpire.objects.get(is_show=True, is_deleted=False, id=expire_id)
                price = float(expire_obj.price)
                # print('xxxxxx',self.id,price) #xxxxxx 1 588.00
        except:
            pass

        active_lists = self.active_list()
        if len(active_lists) > 0:
            active = active_lists[0]        #取第一条活动策略
            sale = active.discount.sale     # 优惠计算公式
            condition = active.discount.condition  # 优惠满足条件 -满多少
            if price > condition:
                if sale == '':
                    price = 0
                elif sale[0] == '*':
                    price = price * float(sale[1:])
                elif sale[0] == '-':
                    price = price - float(sale[1:])
                elif sale[0] == '满':
                    '''
                    满500-80
                    满400-40
                    360
                    满300-20
                    满200-10
                    '''
                    man_list = sale.split('\r\n')
                    con_price_list = [] # 可以满减的条件列表
                    for man in man_list:
                        condition_price,xx_price = man[1:].split('-')
                        if price > float(condition_price):
                            con_price_list.append(float(xx_price))
                    price = price - max(con_price_list)  #取减的最多的那个

        return "%.2f" % price

    @property
    def active_time(self):
        left_time = 0
        active_lists = self.active_list()
        if len(active_lists) > 0:
            active_obj = active_lists[0]
            end_time = active_obj.active.end_time.timestamp()

            now_time = datetime.now().timestamp()
            left_time = end_time - now_time  #剩余时间的时间戳

        return int(left_time)

    @property
    def expire_list(self):
        """课程有效期选项"""
        expires = self.course_expire.filter(is_show=True,is_deleted=False)

        data = []
        for expire in expires:
            data.append({
                'id':expire.id,
                'expire_text':expire.expire_text,
                'price':expire.price,
            })
        # 增加永久有效选项 #如果价格为0就没有永久有效
        if self.price > 0:
            data.append({
                'id': 0,
                'expire_text': '永久有效',
                'price': self.price,
            })

        return data


"""价格相关的模型"""
class CourseDiscountType(BaseModel):
    """课程优惠类型"""
    name = models.CharField(max_length=32, verbose_name="优惠类型名称")
    remark = models.CharField(max_length=250, blank=True, null=True, verbose_name="备注信息")

    class Meta:
        db_table = "ly_course_discount_type"
        verbose_name = "课程优惠类型"
        verbose_name_plural = "课程优惠类型"

    def __str__(self):
        return "%s" % (self.name)

class CourseDiscount(BaseModel):
    """课程优惠策略"""
    discount_type = models.ForeignKey("CourseDiscountType", on_delete=models.CASCADE, related_name='coursediscounts', verbose_name="优惠类型")
    condition = models.IntegerField(blank=True, default=0, verbose_name="满足优惠的价格条件",help_text="设置参与优惠的价格门槛，表示商品必须在xx价格以上的时候才参与优惠活动，<br>如果不填，则不设置门槛") #因为有的课程不足100，你减免100，还亏钱了
    sale = models.TextField(verbose_name="优惠公式",blank=True,null=True, help_text="""
    优惠公式：
    不填表示免费；<br>
    *号开头表示折扣价，例如*0.82表示八二折；<br>
    -号开头则表示减免，例如-20表示原价-20；<br>
    如果需要表示满减,则需要使用 原价-优惠价格,例如表示课程价格大于100,优惠10;大于200,优惠25,格式如下:<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满100-10<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满200-25<br>
    """)

    class Meta:
        db_table = "ly_course_discount"
        verbose_name = "价格优惠策略"
        verbose_name_plural = "价格优惠策略"

    def __str__(self):
        return "价格优惠:%s,优惠条件:%s,优惠值:%s" % (self.discount_type.name, self.condition, self.sale)

class Activity(BaseModel):
    """优惠活动"""
    name = models.CharField(max_length=150, verbose_name="活动名称")
    start_time = models.DateTimeField(verbose_name="优惠策略的开始时间")
    end_time = models.DateTimeField(verbose_name="优惠策略的结束时间")
    remark = models.CharField(max_length=250, blank=True, null=True, verbose_name="备注信息")

    class Meta:
        db_table = "ly_activity"
        verbose_name="商品活动"
        verbose_name_plural="商品活动"

    def __str__(self):
        return self.name

class CoursePriceDiscount(BaseModel):
    """课程与优惠策略的关系表"""
    course = models.ForeignKey("Course",on_delete=models.CASCADE, related_name="activeprices",verbose_name="课程")
    active = models.ForeignKey("Activity",on_delete=models.DO_NOTHING, related_name="activecourses",verbose_name="活动")
    discount = models.ForeignKey("CourseDiscount",on_delete=models.CASCADE,related_name="discountcourse",verbose_name="优惠折扣")

    class Meta:
        db_table = "ly_course_price_dicount"
        verbose_name="课程与优惠策略的关系表"
        verbose_name_plural="课程与优惠策略的关系表"

    def __str__(self):
        return "课程：%s，优惠活动: %s,开始时间:%s,结束时间:%s" % (self.course.name, self.active.name, self.active.start_time,self.active.end_time)


class CourseExpire(BaseModel):
    """课程有效期模型"""
    # 后面可以在数据库把course和expire_time字段设置为联合索引
    course = models.ForeignKey("Course", related_name='course_expire', on_delete=models.CASCADE, verbose_name="课程名称")

    # 有效期限，天数
    expire_time = models.IntegerField(verbose_name="有效期", null=True, blank=True, help_text="有效期按天数计算")

    # 一个月有效等等
    expire_text = models.CharField(max_length=150, verbose_name="提示文本", null=True, blank=True)
    # 每个有效期的价格
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程价格", default=0)

    class Meta:
        db_table = "ly_course_expire"
        verbose_name = "课程有效期"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "课程：%s，有效期：%s，价格：%s" % (self.course, self.expire_text, self.price)





