from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from foods.models import Food
from rest_framework.response import Response
from django_redis import get_redis_connection
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # user_id = 1
        user_id = request.user.id
        redis = get_redis_connection("cart")
        cart_goods_list = redis.hgetall("cart_%s" % user_id)  # 商品课程列表
        cart_goods_selects = redis.smembers("cart_selected_%s" % user_id)
        data_list = []
        # print('cart_goods_list', cart_goods_list)
        # print('cart_goods_selects', cart_goods_selects)
        try:
            for food_id_bytes, expire_bytes in cart_goods_list.items():
                food_id = int(food_id_bytes.decode())
                food = Food.objects.get(pk=food_id)
                # print('food', food)
                try:
                    price = food.price
                except:
                    price = 0

                data_list.append({
                    "id": food_id,
                    "food_img": food.food_img.url,
                    "name": food.name,
                    "price": price,
                    "is_select": food_id_bytes in cart_goods_selects,
                })
        except:
            return Response(data_list, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # print(data_list)
        return Response(data_list, status=status.HTTP_200_OK)

    def post(self, request):
        food_id = request.data.get("food_id")
        try:
            Food.objects.get(pk=food_id, is_delete=False, is_show=True)
        except Food.DoesNotExist:
            return Response({"message": "The current dish does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

        redis = get_redis_connection("cart")
        # user_id = 1
        user_id = request.user.id

        try:
            pipeline = redis.pipeline()
            pipeline.multi()
            pipeline.hset("cart_%s" % user_id, food_id, -1)

            pipeline.sadd("cart_selected_%s" % user_id, food_id)

            pipeline.execute()


        except:
            return Response({"message": "Failed to add dishes to shopping cart! Please contact customer service~"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        count = redis.hlen("cart_%s" % user_id)

        return Response({
            "message": "Successfully added dishes to cart!",
            "count": count,
        }, status=status.HTTP_200_OK)

    def put(self, request):
        """购物车更新商品信息"""
        user_id = request.user.id

        food_id = request.data.get("food_id")
        try:
            Food.objects.get(pk=food_id, is_delete=False, is_show=True)
        except Food.DoesNotExist:
            return Response({"message": "The current dish does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

        is_select = request.data.get("is_select")

        redis = get_redis_connection("cart")

        if is_select:
            redis.sadd("cart_selected_%s" % user_id, food_id)
        else:
            redis.srem("cart_selected_%s" % user_id, food_id)

        return Response({
            "message": "Succeeded in modifying shopping cart information!"
        }, status=status.HTTP_200_OK)

    def patch(self, request):

        user_id = request.user.id

        food_id = request.data.get("food_id")

        course = Food.objects.get(pk=food_id)
        price = course.price

        return Response({
            "price": price,
            "message": "Succeeded in modifying shopping cart information!"
        }, status=status.HTTP_200_OK)

    def delete(self, request):

        user_id = request.user.id
        # print(user_id)
        food_id = request.query_params.get("food_id")
        # print(food_id)
        redis = get_redis_connection("cart")
        pipeline = redis.pipeline()

        pipeline.multi()
        pipeline.hdel("cart_%s" % user_id, food_id)
        pipeline.srem("cart_selected_%s" % user_id, food_id)
        pipeline.execute()

        return Response({"message": "Delete dishes course successfully!"}, status=status.HTTP_204_NO_CONTENT)
