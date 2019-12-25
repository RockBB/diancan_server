from django.db import models

# Create your models here.
from diancan_server.utils.models import BaseModel
from users.models import User
from foods.models import Food


class Order(BaseModel):
    """订单记录"""
    status_choices = (
        (0, '未支付'),
        (1, '已支付'),
        (2, '已取消'),
        (3, '超时取消'),
    )
    pay_choices = (
        (0, '会员账户支付'),
        (1, '支付宝'),
        (2, '微信支付')
    )
    order_title = models.CharField(max_length=150, verbose_name="订单标题")
    total_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="订单总价", default=0)
    real_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="实付金额", default=0)
    order_number = models.CharField(max_length=64, verbose_name="订单号")
    order_status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="订单状态")
    pay_type = models.SmallIntegerField(choices=pay_choices, default=0, verbose_name="支付方式")
    use_coupon = models.BooleanField(default=False, verbose_name="是否使用优惠券")
    coupon = models.IntegerField(null=True, verbose_name="用户优惠券ID")
    order_desc = models.TextField(max_length=500, null=True, blank=True, verbose_name="订单描述")
    pay_time = models.DateTimeField(null=True, verbose_name="支付时间")
    user = models.ForeignKey(User, related_name='user_orders', on_delete=models.DO_NOTHING, verbose_name="下单用户")

    class Meta:
        db_table = "dc_order"
        verbose_name = "订单记录"
        verbose_name_plural = "订单记录"

    def __str__(self):
        return "%s,总价: %s,实付: %s" % (self.order_title, self.total_price, self.real_price)

    def order_status_text(self):
        return self.status_choices[self.order_status][1]


class OrderDetail(BaseModel):
    """订单详情"""
    order = models.ForeignKey(Order, related_name='order_foods', on_delete=models.CASCADE, verbose_name="订单")
    food = models.ForeignKey(Food, related_name='foods_orders', on_delete=models.CASCADE, verbose_name="食物")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="食物原价")
    real_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="食物实价")
    discount_name = models.CharField(max_length=120, default="", verbose_name="优惠活动类型")

    class Meta:
        db_table = "dc_order_detail"
        verbose_name = "订单详情"
        verbose_name_plural = "订单详情"

    def food_img(self):
        # 返回图片的url地址
        return self.food.food_img.url

    def food_name(self):
        return self.food.name
