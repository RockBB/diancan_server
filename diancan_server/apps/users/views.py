from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserModelSerializer, UserMoneySerializer
from rest_framework.generics import CreateAPIView
from .models import User


class UserMoneyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserMoneySerializer
    queryset = User.objects.all()

    def post(self, request):
        """购物车更新商品信息"""
        # 获取当前登录用户ID
        user_id = request.user.id

        # 获取客户端发送过来的课程ID
        money = request.data.get("money")
        # print(money)
        try:

            user_money = User.objects.get(id=user_id).money
            # print('user_money', user_money, type(user_money))
            money = float(user_money) - float(money)
            ret = User.objects.filter(id=user_id).update(money=money, is_active=True)
            # print('', ret, type(ret))
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'money': money}, status=status.HTTP_200_OK)


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


