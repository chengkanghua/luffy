from django.db import models

class BaseModel(models.Model):
    """公共模型"""
    is_show = models.BooleanField(default=False, verbose_name="是否显示")
    orders = models.IntegerField(default=1, verbose_name="排序")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
		#更新：update方法不能自动更新auto_now的时间，save()方法保存能够自动修改更新时间
    class Meta:
        # 设置当前模型为抽象模型，在数据迁移的时候django就不会为它单独创建一张表
        abstract = True