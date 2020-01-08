from rest_framework import serializers
from .models import User
import re

class UserMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "money")

class UserModelSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, help_text="Confirm password")
    token = serializers.CharField(read_only=True, help_text="jwt token值")

    class Meta:
        model = User
        # fields = ["mobile","sms_code","id","token"]
        fields = ["mobile", "id", "token", "password", "password2", "username"]
        extra_kwargs = {
            "id": {"read_only": True},
            "username": {"read_only": True},
            "password": {"write_only": True},
            "mobile": {"write_only": True}
        }

    def validate_mobile(self, mobile):
        result = re.match('^1[3-9]\d{9}$', mobile)
        if not result:
            raise serializers.ValidationError("Wrong format of mobile number!")

        try:
            user = User.objects.get(mobile=mobile)
            if user:
                raise serializers.ValidationError("The current mobile number has been registered!")

        except User.DoesNotExist:
            pass

        return mobile

    def validate(self, attrs):

        password = attrs.get("password")
        if not re.match('^.{6,16}$', password):
            raise serializers.ValidationError("Password length must be between 6-16 bits!")

        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError("Password and confirm password are inconsistent!")

        return attrs

    def create(self, validated_data):
        mobile = validated_data.get("mobile")
        password = validated_data.get("password")

        try:
            user = User.objects.create(
                mobile=mobile,
                username=mobile,
                password=password,
            )

            user.set_password(user.password)
            user.save()

        except:
            raise serializers.ValidationError("Failed to register user!")

        from rest_framework_jwt.settings import api_settings

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)

        return user


from orders.models import Order, OrderDetail


class OrderDetailListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ("price", "real_price", "food_img", "food_name", "food")


class OrderListModelSerializer(serializers.ModelSerializer):
    order_foods = OrderDetailListModelSerializer(many=True)

    class Meta:
        model = Order
        fields = (
        "order_foods", "id", "create_time", "pay_time", "order_number", "real_price", "total_price", "order_status",
        "order_status_text", "pay_type")


class UserOrderModelSerializer(serializers.ModelSerializer):
    user_orders = OrderListModelSerializer(many=True)

    class Meta:
        model = User
        fields = ("username", "user_orders")
