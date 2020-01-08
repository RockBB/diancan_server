from django.db import models

from diancan_server.utils.models import BaseModel
from datetime import datetime
from decimal import Decimal


class FoodCategory(BaseModel):

    name = models.CharField(max_length=64, unique=True, verbose_name="Category Name")

    class Meta:
        db_table = "dc_food_category"
        verbose_name = "Food Category"
        verbose_name_plural = "Food Category"

    def __str__(self):
        return "%s" % self.name


from ckeditor_uploader.fields import RichTextUploadingField


class Food(BaseModel):

    name = models.CharField(max_length=128, verbose_name="Food Name")
    food_img = models.ImageField(upload_to="food", max_length=255, verbose_name="Food images", blank=True, null=True)   # 菜品图片
    brief = RichTextUploadingField(max_length=2048, verbose_name="Brief", null=True, blank=True)
    pub_date = models.DateField(verbose_name="Publish Date", auto_now_add=True)
    food_category = models.ForeignKey("FoodCategory", on_delete=models.CASCADE, null=True, blank=True,
                                      verbose_name="Food Category")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Price", default=0)

    class Meta:
        db_table = "dc_food"
        verbose_name = "Food Details"
        verbose_name_plural = "Food Details"

    def __str__(self):
        return "%s" % self.name




