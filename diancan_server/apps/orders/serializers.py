from rest_framework import serializers
from .models import Order, OrderDetail


class OrderFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        # fields = ("__all__")
        fields = ("id", "food_name", "price", "real_price",
                  "discount_name",
                  "food_img",
                  "food_name",)


class OrderDetailModelSerializer(serializers.ModelSerializer):
    order_foods = OrderFoodSerializer(many=True)

    class Meta:
        model = Order
        # fields = ("__all__")
        fields = ("order_title", "total_price", "order_number",
                  "order_status",
                  "pay_type",
                  "pay_time",
                  "user", "order_foods")
