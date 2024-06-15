from django.db import models


class BaseModel(models.Model):
    # 将来轮播图肯定会更新，到底显示哪些
    is_show = models.BooleanField(default=False, verbose_name="是否显示")
    orders = models.IntegerField(default=1, verbose_name="排序")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    class Meta:
        # 数据库迁移时，设置了bstract = True的model类不会生成数据库表
        abstract = True