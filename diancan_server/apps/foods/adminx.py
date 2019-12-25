import xadmin

from .models import FoodCategory


class FoodCategoryModelAdmin(object):
    """课程分类模型管理类"""
    pass


xadmin.site.register(FoodCategory, FoodCategoryModelAdmin)

from .models import Food


class FoodModelAdmin(object):
    """课程模型管理类"""
    pass


xadmin.site.register(Food, FoodModelAdmin)
