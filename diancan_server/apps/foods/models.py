from django.db import models

from diancan_server.utils.models import BaseModel
from datetime import datetime
from decimal import Decimal


class FoodCategory(BaseModel):
    """
    课程分类
    """
    name = models.CharField(max_length=64, unique=True, verbose_name="Category Name")   # 分类名称

    class Meta:
        db_table = "dc_food_category"
        # verbose_name = "食物分类"
        verbose_name = "Food Category"
        # verbose_name_plural = "食物分类"
        verbose_name_plural = "Food Category"

    def __str__(self):
        return "%s" % self.name


from ckeditor_uploader.fields import RichTextUploadingField


class Food(BaseModel):
    """食物详情"""

    name = models.CharField(max_length=128, verbose_name="Food Name")   # 食物名称
    food_img = models.ImageField(upload_to="food", max_length=255, verbose_name="Food images", blank=True, null=True)   # 菜品图片
    # 使用这个字段的原因
    brief = RichTextUploadingField(max_length=2048, verbose_name="Brief", null=True, blank=True)   # 详情介绍
    pub_date = models.DateField(verbose_name="Publish Date", auto_now_add=True)   # 发布日期
    food_category = models.ForeignKey("FoodCategory", on_delete=models.CASCADE, null=True, blank=True,
                                      verbose_name="Food Category")   # 食物分类
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Price", default=0)   # 食物原价
    # teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="授课老师")

    class Meta:
        db_table = "dc_food"
        verbose_name = "Food Details"
        verbose_name_plural = "Food Details"

    def __str__(self):
        return "%s" % self.name




