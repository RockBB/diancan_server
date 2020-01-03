import xadmin

# from .models import User
#
#
# class UserModelAdmin(object):
#     """订单模型管理类"""
#     pass
#
#
# xadmin.site.register(User, UserModelAdmin)

from .models import UserFood


class UserFoodModelAdmin(object):
    """订单详情模型管理类"""
    pass


xadmin.site.register(UserFood, UserFoodModelAdmin)
