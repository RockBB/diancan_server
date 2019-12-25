from rest_framework import serializers
from .models import Order,OrderDetail

class OrderFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        #fields = ("__all__")
        fields = ("id", "food_name", "price")

class OrderDetailModelSerializer(serializers.ModelSerializer):
    order_foods = OrderFoodSerializer(many=True)
    class Meta:
        model = Order
        fields = ("__all__")
        #fields = ("order_title","total_price")