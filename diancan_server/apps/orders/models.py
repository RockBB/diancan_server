from django.db import models

# Create your models here.
from diancan_server.utils.models import BaseModel
from users.models import User
from foods.models import Food


class Order(BaseModel):
    status_choices = (
        (0, 'Unpaid'),
        (1, 'Paid'),
        (2, 'Cancelled'),
        (3, 'Timeout'),
    )
    pay_choices = (
        (0, 'VIP Account '),
        (1, 'Alipay'),
        (2, 'Wchart')
    )
    order_title = models.CharField(max_length=150, verbose_name="Order Title")
    total_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Total Price", default=0)
    real_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Real Price", default=0)
    order_number = models.CharField(max_length=64, verbose_name="Order Number")
    order_status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="Order Status")
    pay_type = models.SmallIntegerField(choices=pay_choices, default=0, verbose_name="Pay Type")
    use_coupon = models.BooleanField(default=False, verbose_name="Pay Type")
    coupon = models.IntegerField(null=True, verbose_name="coupon")
    order_desc = models.TextField(max_length=500, null=True, blank=True, verbose_name="Order Desc")
    pay_time = models.DateTimeField(null=True, verbose_name="Pay Time")
    user = models.ForeignKey(User, related_name='user_orders', on_delete=models.DO_NOTHING, verbose_name="User")

    class Meta:
        db_table = "dc_order"
        verbose_name = "Order Record"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,total price: %s,real price: %s" % (self.order_title, self.total_price, self.real_price)

    def order_status_text(self):
        return self.status_choices[self.order_status][1]


class OrderDetail(BaseModel):
    """订单详情"""
    order = models.ForeignKey(Order, related_name='order_foods', on_delete=models.CASCADE, verbose_name="Order")
    food = models.ForeignKey(Food, related_name='foods_orders', on_delete=models.CASCADE, verbose_name="Food")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Price")
    real_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Real Rrice")
    discount_name = models.CharField(max_length=120, default="", verbose_name="Discount Type")

    class Meta:
        db_table = "dc_order_detail"
        verbose_name = "Order Detail"
        verbose_name_plural = verbose_name

    def food_img(self):
        return self.food.food_img.url

    def food_name(self):
        return self.food.name
