from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserModelSerializer, UserMoneySerializer
from rest_framework.generics import CreateAPIView
from .models import User
from orders.models import Order
import datetime
from django.db import transaction
from decimal import Decimal
from datetime import datetime
from users.models import UserFood
import logging
log = logging.getLogger("django")


class UserMoneyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # serializer_class = UserMoneySerializer
    queryset = User.objects.all()

    def get(self, request):
        """获取购物车商品课程列表"""
        # 获取当前用户ID
        # user_id = 1
        user_id = request.user.id
        if user_id:
            user_money = User.objects.get(id=user_id).money
            return Response({"money": user_money}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "无效的请求"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """购物车更新商品信息"""
        # 获取当前登录用户ID
        user_id = request.user.id
        # print(user_id)
        # 获取客户端发送过来的课程ID
        money = request.data.get("money")
        order_number = request.data.get("order_number")
        # print(money)
        try:

            user_money = User.objects.get(id=user_id).money
            # print('user_money', user_money, type(user_money))
            money = Decimal(user_money) - Decimal(money)
            ret = User.objects.filter(id=user_id).update(money=money, is_active=True)
            # print('', ret, type(ret))

            try:
                order = Order.objects.get(order_number=order_number)
                # print('order', order)
            except Order.DoesNotExist:
                log.error("订单号:%s不存在!" % order_number )
                return Response({"message": "无效的订单号"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            dt = datetime.now()
            with transaction.atomic():
                save_id = transaction.savepoint()
                order.order_status = 1
                order.pay_time = datetime.now()
                order.save()

                # 课程与用户之间添加一条购买记录
                detail_list = order.order_foods.all()
                course_list = []
                for detail in detail_list:
                    # print('ddd', detail)
                    UserFood.objects.create(user=order.user,food=detail.food,
                                            buy_number=order_number,buy_type=0,
                                            pay_time=dt.strftime('%Y-%m-%d %H:%M:%S'),)

                    course_list.append(detail.food.name)

            return Response({'money': money, 'success': 'pay success'}, status=status.HTTP_200_OK)

        except:
            # log.error("修改订单和购买记录发生异常!")
            transaction.savepoint_rollback(save_id)
            return Response({"message":"系统异常!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserAPIView(CreateAPIView):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()



from .serializers import UserOrderModelSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated


class UserOrderAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserOrderModelSerializer
    queryset = User.objects.all()


