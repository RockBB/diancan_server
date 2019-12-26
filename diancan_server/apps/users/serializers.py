from rest_framework import serializers
from .models import User
import re


class UserModelSerializer(serializers.ModelSerializer):
    # sms_code = serializers.CharField(max_length=6,min_length=6,required=True,help_text="短信验证码")
    password2 = serializers.CharField(write_only=True, help_text="确认密码")
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
        # 验证格式
        result = re.match('^1[3-9]\d{9}$', mobile)
        if not result:
            raise serializers.ValidationError("手机号码格式有误!")

        # 验证唯一性
        try:
            user = User.objects.get(mobile=mobile)
            if user:
                raise serializers.ValidationError("当前手机号码已经被注册!")

        except User.DoesNotExist:
            pass

        return mobile

    def validate(self, attrs):

        # 判断密码长度
        password = attrs.get("password")
        if not re.match('^.{6,16}$', password):
            raise serializers.ValidationError("密码长度必须在6-16位之间!")

        # 判断密码和确认密码是否一致
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError("密码和确认密码不一致!")

        return attrs

    def create(self, validated_data):
        """保存用户"""
        mobile = validated_data.get("mobile")
        password = validated_data.get("password")

        try:
            user = User.objects.create(
                mobile=mobile,
                username=mobile,
                password=password,
            )

            # 密码加密
            user.set_password(user.password)
            user.save()

        except:
            raise serializers.ValidationError("注册用户失败!")

        # 生成一个jwt
        from rest_framework_jwt.settings import api_settings

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)

        return user


"""会员订单"""
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
        # fields = ("username","身份信息..")
        fields = ("username", "user_orders")
