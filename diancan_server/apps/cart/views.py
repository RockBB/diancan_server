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
    """购物车视图"""

    def get(self, request):
        """获取购物车商品课程列表"""
        # 获取当前用户ID
        # user_id = 1
        user_id = request.user.id
        # 通过用户ID获取购物车中的商品信息
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
        # 返回查询结果
        return Response(data_list, status=status.HTTP_200_OK)

    def post(self, request):
        """购物车添加商品"""
        # 获取客户端发送过来的课程ID
        food_id = request.data.get("food_id")
        # 验证课程ID是否有效
        try:
            Food.objects.get(pk=food_id, is_delete=False, is_show=True)
        except Food.DoesNotExist:
            return Response({"message": "The current dish does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

        # 组装基本数据[课程ID,有效期]保存到redis
        redis = get_redis_connection("cart")
        # user_id = 1
        user_id = request.user.id

        try:
            # 创建事务[管道]对象
            pipeline = redis.pipeline()
            # 开启事务
            pipeline.multi()
            # 添加一个成员到指定名称的hash数据中[如果对应名称的hash数据不存在,则自动创建]
            # hset(名称,键,值)
            pipeline.hset("cart_%s" % user_id, food_id, -1)  # -1表示购买的课程永久有效

            # 添加一个成员到制定名称的set数据中[如果对应名称的set数据不存在,则自动创建]
            # sadd(名称,成员)
            pipeline.sadd("cart_selected_%s" % user_id, food_id)

            # 提交事务[如果不提交,则事务会自动回滚]
            pipeline.execute()


        except:
            return Response({"message": "Failed to add dishes to shopping cart! Please contact customer service~"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        # 返回结果,返回购物车中的商品数量
        count = redis.hlen("cart_%s" % user_id)

        return Response({
            "message": "Successfully added dishes to cart!",
            "count": count,
        }, status=status.HTTP_200_OK)

    def put(self, request):
        """购物车更新商品信息"""
        # 获取当前登录用户ID
        user_id = request.user.id

        # 获取客户端发送过来的课程ID
        food_id = request.data.get("food_id")
        # 验证课程ID是否有效
        try:
            Food.objects.get(pk=food_id, is_delete=False, is_show=True)
        except Food.DoesNotExist:
            return Response({"message": "The current dish does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

        # 获取勾选状态
        is_select = request.data.get("is_select")
        # print('----------', is_select, course_id, type(is_select))
        # 链接redis
        redis = get_redis_connection("cart")

        # 修改购物车中指定商品课程的信息
        if is_select:
            # 从勾选集合中新增一个课程ID
            redis.sadd("cart_selected_%s" % user_id, food_id)
        else:
            redis.srem("cart_selected_%s" % user_id, food_id)

        return Response({
            "message": "Succeeded in modifying shopping cart information!"
        }, status=status.HTTP_200_OK)

    def patch(self, request):
        """更新购物城中的商品信息[切换课程有效期]"""
        # 获取当前登录的用户ID
        # user_id = 1
        user_id = request.user.id

        # 获取当前操作的课程ID
        food_id = request.data.get("food_id")

        course = Food.objects.get(pk=food_id)
        price = course.price

        return Response({
            "price": price,
            "message": "Succeeded in modifying shopping cart information!"
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        """从购物车中删除数据"""
        # 获取当前登录用户ID
        # user_id = 1
        user_id = request.user.id
        # print(user_id)
        # 获取课程ID
        food_id = request.query_params.get("food_id")
        # print(food_id)
        redis = get_redis_connection("cart")
        pipeline = redis.pipeline()

        pipeline.multi()
        # 从购物车中删除指定商品课程
        pipeline.hdel("cart_%s" % user_id, food_id)

        # 从勾选集合中移除指定商品课程
        pipeline.srem("cart_selected_%s" % user_id, food_id)

        pipeline.execute()

        # 返回操作结果
        return Response({"message": "Delete dishes course successfully!"}, status=status.HTTP_204_NO_CONTENT)
