# -*- coding: utf-8 -*-
# __author: rock
# @time: 2019-12-24
from django.db import models


class BaseModel(models.Model):
    """公共字段模型"""
    orders = models.IntegerField(verbose_name='Display Order', null=True, blank=True)  # 显示顺序
    is_show = models.BooleanField(verbose_name="Is Show", default=False)  # 是否上架
    is_delete = models.BooleanField(verbose_name="Is Delete", default=False)  # 逻辑删除
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")  # 添加时间
    update_time = models.DateTimeField(auto_now=True, verbose_name="Update Time")  # 更新时间

    class Meta:
        # 设置当前模型在数据迁移的时候不要为它创建表
        abstract = True
