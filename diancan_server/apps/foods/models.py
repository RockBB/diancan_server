from django.db import models

from diancan_server.utils.models import BaseModel
from datetime import datetime
from decimal import Decimal


class FoodCategory(BaseModel):
    """
    课程分类
    """
    name = models.CharField(max_length=64, unique=True, verbose_name="分类名称")

    class Meta:
        db_table = "dc_food_category"
        verbose_name = "食物分类"
        verbose_name_plural = "食物分类"

    def __str__(self):
        return "%s" % self.name


from ckeditor_uploader.fields import RichTextUploadingField


class Food(BaseModel):
    """食物详情"""

    name = models.CharField(max_length=128, verbose_name="食物名称")
    food_img = models.ImageField(upload_to="food", max_length=255, verbose_name="菜品图片", blank=True, null=True)
    # 使用这个字段的原因
    brief = RichTextUploadingField(max_length=2048, verbose_name="详情介绍", null=True, blank=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)
    food_category = models.ForeignKey("FoodCategory", on_delete=models.CASCADE, null=True, blank=True,
                                      verbose_name="食物分类")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="食物原价", default=0)
    # teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="授课老师")

    class Meta:
        db_table = "dc_food"
        verbose_name = "食物详情"
        verbose_name_plural = "食物详情"

    def __str__(self):
        return "%s" % self.name




