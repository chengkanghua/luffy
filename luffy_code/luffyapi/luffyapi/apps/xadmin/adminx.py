from __future__ import absolute_import
import xadmin
from .models import UserSettings, Log

from django.utils.translation import ugettext_lazy as _


class UserSettingsAdmin(object):
    model_icon = 'fa fa-cog'
    hidden_menu = True

xadmin.site.register(UserSettings, UserSettingsAdmin)

class LogAdmin(object):

    def link(self, instance):
        if instance.content_type and instance.object_id and instance.action_flag != 'delete':
            admin_url = self.get_admin_url('%s_%s_change' % (instance.content_type.app_label, instance.content_type.model), 
                instance.object_id)
            return "<a href='%s'>%s</a>" % (admin_url, _('Admin Object'))
        else:
            return ''
    link.short_description = ""
    link.allow_tags = True
    link.is_column = False

    list_display = ('action_time', 'user', 'ip_addr', '__str__', 'link')
    list_filter = ['user', 'action_time']
    search_fields = ['ip_addr', 'message']
    model_icon = 'fa fa-cog'

xadmin.site.register(Log, LogAdmin)

import xadmin
from xadmin import views

class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)

class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "路飞学城"  # 设置站点标题
    site_footer = "路飞学城有限公司"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠

xadmin.site.register(views.CommAdminView, GlobalSettings)

# 轮播图
from home.models import Banner

class BannerModelAdmin(object):
    list_display = ["title", "orders", "is_show"]

xadmin.site.register(Banner, BannerModelAdmin)

# 导航菜单
from home.models import Nav
class NavModelAdmin(object):
    list_display=["title","link","is_show","is_site","position"]
xadmin.site.register(Nav, NavModelAdmin)


from course.models import CourseCategory
class CourseCategoryModelAdmin(object):
    """课程分类模型管理类"""
    pass
xadmin.site.register(CourseCategory, CourseCategoryModelAdmin)


from course.models import Course
class CourseModelAdmin(object):
    """课程模型管理类"""
    pass
xadmin.site.register(Course, CourseModelAdmin)


from course.models import Teacher
class TeacherModelAdmin(object):
    """老师模型管理类"""
    pass
xadmin.site.register(Teacher, TeacherModelAdmin)


from course.models import CourseChapter
class CourseChapterModelAdmin(object):
    """课程章节模型管理类"""
    pass
xadmin.site.register(CourseChapter, CourseChapterModelAdmin)



from course.models import CourseLesson
class CourseLessonModelAdmin(object):
    """课程课时模型管理类"""
    pass
xadmin.site.register(CourseLesson, CourseLessonModelAdmin)

from course.models import CourseDiscountType
class CourseExpireModelAdmin(object):
    """课程与有效期模型管理类"""
    pass
xadmin.site.register(CourseDiscountType, CourseExpireModelAdmin)

from course.models import CourseDiscount
class PriceDiscountTypeModelAdmin(object):
    """价格优惠类型"""
    pass
xadmin.site.register(CourseDiscount, PriceDiscountTypeModelAdmin)


from course.models import Activity
class PriceDiscountModelAdmin(object):
    """价格优惠公式"""
    pass
xadmin.site.register(Activity, PriceDiscountModelAdmin)


from course.models import CoursePriceDiscount
class CoursePriceDiscountModelAdmin(object):
    """商品优惠和活动的关系"""
    pass
xadmin.site.register(CoursePriceDiscount, CoursePriceDiscountModelAdmin)

from course.models import CourseExpire
class CourseExpireModelAdmin(object):
    """商品有效期模型"""
    pass
xadmin.site.register(CourseExpire, CourseExpireModelAdmin)