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

        user_id = request.user.id

        order_number = datetime.now().strftime("%Y%m%d%H%M%S") + "%08d" % user_id + "%04d" % random.randint(0, 9999)

        with transaction.atomic():

            save_id = transaction.savepoint()

            try:
                order = Order.objects.create(order_title="Food purchase", total_price=0, real_price=0,
                                             order_number=order_number, user_id=user_id, )

                redis = get_redis_connection("cart")
                food_selects_set = redis.smembers("cart_selected_%s" % user_id)
                if food_selects_set:
                    # print( course_selects_set )
                    cart_food_list = redis.hgetall("cart_%s" % user_id)
                    total_price = 0

                    pipeline = redis.pipeline()
                    pipeline.multi()

                    for food_id_byte, expire_byte in cart_food_list.items():
                        if food_id_byte in food_selects_set:
                            expire = expire_byte.decode()
                            food_id = food_id_byte.decode()
                            food = Food.objects.get(pk=food_id)
                            food_price = food.price
                            total_price += food_price

                            OrderDetail.objects.create(
                                order_id=order.id,
                                food_id=food_id,
                                price=food_price,
                                real_price=food_price,
                            )

                            pipeline.srem("cart_selected_%s" % user_id, food_id)
                            pipeline.hdel("cart_%s" % user_id, food_id)

                    pipeline.execute()
                    order.total_price = total_price
                    order.real_price = total_price
                    order.save()
                else:
                    return Response(
                        {"message": "Failed to generate the order. You have not selected any items in the shopping cart!"},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

            except Exception:
                log.error("%s" % Exception)
                transaction.savepoint_rollback(save_id)
                return Response({"message": "System exception!"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

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
