from luffyapi.utils.models import BaseModel
from django.db import models
# Create your models here.
class Banner(BaseModel):
    """轮播广告图模型"""
    # 模型字段
    title = models.CharField(max_length=500, verbose_name="广告标题")
    link = models.CharField(max_length=500, verbose_name="广告链接")
    # upload_to 设置上传文件的保存子目录,将来上传来的文件会存到我们的media下面的banner文件夹下，这里存的是图片地址。
    image_url =  models.ImageField(upload_to="banner", null=True, blank=True, max_length=255, verbose_name="广告图片")

    remark = models.TextField(verbose_name="备注信息")


    # 表信息声明
    class Meta:
        db_table = "ly_banner"
        verbose_name = "轮播广告"
        verbose_name_plural = verbose_name

    # 自定义方法[自定义字段或者自定义工具方法]
    def __str__(self):
        return self.title


class Nav(BaseModel):
    """导航菜单模型"""
    POSITION_OPTION = (
        (1, "顶部导航"),
        (2, "脚部导航"),
    )
    title = models.CharField(max_length=500, verbose_name="导航标题")
    link = models.CharField(max_length=500, verbose_name="导航链接")
    position = models.IntegerField(choices=POSITION_OPTION, default=1, verbose_name="导航位置")
    is_site = models.BooleanField(default=False, verbose_name="是否是站外地址")

    class Meta:
        db_table = 'ly_nav'
        verbose_name = '导航菜单'
        verbose_name_plural = verbose_name

    # 自定义方法[自定义字段或者自定义工具方法]
    def __str__(self):
        return self.title






