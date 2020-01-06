from django.contrib.auth.models import AbstractUser
from django.db import models
from diancan_server.utils.models import BaseModel


class User(AbstractUser):
    """用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='phone number')
    money = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Account amount", default=0)

    class Meta:
        db_table = 'dc_users'
        # verbose_name = '用户'
        verbose_name = 'User'
        verbose_name_plural = verbose_name


# from diancan_server.utils.models import BaseModel


from foods.models import Food


class UserFood(BaseModel):
    pay_choices = (
        (0, 'VIP Account '),   # 会员账户支付
        (1, 'Alipay'),   # 支付宝
        (2, 'Wchart'),   # 微信支付
        (3, 'Free activities'),  # 免费活动
        (4, 'Movable gifts'),  # 活动赠品
    )
    user = models.ForeignKey(User, related_name='user_cp', on_delete=models.DO_NOTHING, verbose_name="User")  # 用户
    food = models.ForeignKey(Food, related_name='foods_users', on_delete=models.DO_NOTHING, verbose_name="Food")  # 课程
    buy_number = models.CharField(max_length=128, null=True, verbose_name="Buy Number")  # 账单号
    buy_type = models.SmallIntegerField(choices=pay_choices, default=0, verbose_name="Buy Type")  # 购买方式
    pay_time = models.DateTimeField(null=True, verbose_name="Pay Time")  # 购买时间

    class Meta:
        db_table = 'dc_user'
        # verbose_name = '点菜记录'
        verbose_name = 'User Order'
        verbose_name_plural = verbose_name
