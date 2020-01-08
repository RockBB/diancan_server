import xadmin

# from .models import User
#
#
# class UserModelAdmin(object):
#     pass
#
#
# xadmin.site.register(User, UserModelAdmin)

from .models import UserFood


class UserFoodModelAdmin(object):
    pass


xadmin.site.register(UserFood, UserFoodModelAdmin)
