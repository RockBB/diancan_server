from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django_redis import get_redis_connection
from rest_framework.response import Response
from .models import Order, OrderDetail
from datetime import datetime
from foods.models import Food
import random
from django.db import transaction
from rest_framework import status

import logging

log = logging.getLogger("django")


class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """生成订单"""
        # 获取用户ID
        # user_id = 1
        user_id = request.user.id

        # 订单号,必须保证唯一
        order_number = datetime.now().strftime("%Y%m%d%H%M%S") + "%08d" % user_id + "%04d" % random.randint(0, 9999)

        with transaction.atomic():

            # 数据库事务的回滚标记
            save_id = transaction.savepoint()

            # 生成空的订单
            try:
                order = Order.objects.create(order_title="Food purchase", total_price=0, real_price=0,
                                             order_number=order_number, user_id=user_id, )

                # 到redis获取购物车信息
                redis = get_redis_connection("cart")
                # 勾选状态
                food_selects_set = redis.smembers("cart_selected_%s" % user_id)
                if food_selects_set:
                    # print( course_selects_set )
                    # 购物车中商品课程列表
                    cart_food_list = redis.hgetall("cart_%s" % user_id)
                    # 回滚事务
                    # 通过购物车信息到数据中提取相关数据
                    # 计算订单总价
                    total_price = 0

                    # 开启redis的管道操作[事务操作]
                    pipeline = redis.pipeline()
                    pipeline.multi()

                    for food_id_byte, expire_byte in cart_food_list.items():
                        if food_id_byte in food_selects_set:
                            expire = expire_byte.decode()
                            food_id = food_id_byte.decode()
                            food = Food.objects.get(pk=food_id)
                            food_price = food.price
                            total_price += food_price

                            # 生成订单详情
                            OrderDetail.objects.create(
                                order_id=order.id,
                                food_id=food_id,
                                price=food_price,
                                real_price=food_price,
                            )

                            # 从购物车中移除已经加入订单的商品
                            pipeline.srem("cart_selected_%s" % user_id, food_id)
                            pipeline.hdel("cart_%s" % user_id, food_id)

                    # 提交redis的事务操作
                    pipeline.execute()
                    # 补充订单的总价格
                    order.total_price = total_price
                    order.real_price = total_price
                    order.save()
                else:
                    return Response(
                        {"message": "Failed to generate the order. You have not selected any items in the shopping cart!"},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

            except Exception:
                # 记录错误日志
                log.error("%s" % Exception)
                # 回滚事务
                transaction.savepoint_rollback(save_id)
                # 响应结果
                return Response({"message": "System exception!"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        # 响应结果
        return Response({"message": "Order generated successfully!", "order": order.order_number})


from .serializers import OrderDetailModelSerializer


class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(order_number=pk)
        except Order.DoesNotExist:
            return Response({"message": "Wrong order information!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderDetailModelSerializer(instance=order)

        return Response(serializer.data, status=status.HTTP_200_OK)
