from django.contrib.auth.models import AbstractUser
from django.db import models
from diancan_server.utils.models import BaseModel


class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name='phone number')
    money = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Account amount", default=0)

    class Meta:
        db_table = 'dc_users'
        verbose_name = 'User'
        verbose_name_plural = verbose_name


# from diancan_server.utils.models import BaseModel


from foods.models import Food


class UserFood(BaseModel):
    pay_choices = (
        (0, 'VIP Account '),
        (1, 'Alipay'),
        (2, 'Wchart'),
        (3, 'Free activities'),
        (4, 'Movable gifts'),
    )
    user = models.ForeignKey(User, related_name='user_cp', on_delete=models.DO_NOTHING, verbose_name="User")
    food = models.ForeignKey(Food, related_name='foods_users', on_delete=models.DO_NOTHING, verbose_name="Food")
    buy_number = models.CharField(max_length=128, null=True, verbose_name="Buy Number")
    buy_type = models.SmallIntegerField(choices=pay_choices, default=0, verbose_name="Buy Type")
    pay_time = models.DateTimeField(null=True, verbose_name="Pay Time")

    class Meta:
        db_table = 'dc_user'
        verbose_name = 'User Order'
        verbose_name_plural = verbose_name
