import xadmin

from .models import FoodCategory


class FoodCategoryModelAdmin(object):
    pass


xadmin.site.register(FoodCategory, FoodCategoryModelAdmin)

from .models import Food


class FoodModelAdmin(object):
    pass


xadmin.site.register(Food, FoodModelAdmin)
