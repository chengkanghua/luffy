import xadmin

from .models import CourseCategory
class CourseCategoryModelAdmin(object):
    """课程分类模型管理类"""
    pass
xadmin.site.register(CourseCategory, CourseCategoryModelAdmin)


from .models import Course
class CourseModelAdmin(object):
    """课程模型管理类"""
    pass
xadmin.site.register(Course, CourseModelAdmin)


from .models import Teacher
class TeacherModelAdmin(object):
    """老师模型管理类"""
    pass
xadmin.site.register(Teacher, TeacherModelAdmin)


from .models import CourseChapter
class CourseChapterModelAdmin(object):
    """课程章节模型管理类"""
    pass
xadmin.site.register(CourseChapter, CourseChapterModelAdmin)



from .models import CourseLesson
class CourseLessonModelAdmin(object):
    """课程课时模型管理类"""
    pass
xadmin.site.register(CourseLesson, CourseLessonModelAdmin)



from .models import CourseDiscountType
class CourseExpireModelAdmin(object):
    """课程与有效期模型管理类"""
    pass
xadmin.site.register(CourseDiscountType, CourseExpireModelAdmin)

from .models import CourseDiscount
class PriceDiscountTypeModelAdmin(object):
    """价格优惠类型"""
    pass
xadmin.site.register(CourseDiscount, PriceDiscountTypeModelAdmin)


from .models import Activity
class PriceDiscountModelAdmin(object):
    """价格优惠公式"""
    pass
xadmin.site.register(Activity, PriceDiscountModelAdmin)


from .models import CoursePriceDiscount
class CoursePriceDiscountModelAdmin(object):
    """商品优惠和活动的关系"""
    pass
xadmin.site.register(CoursePriceDiscount, CoursePriceDiscountModelAdmin)


from .models import CourseExpire
class CourseExpireModelAdmin(object):
    """商品有效期模型"""
    pass
xadmin.site.register(CourseExpire, CourseExpireModelAdmin)



