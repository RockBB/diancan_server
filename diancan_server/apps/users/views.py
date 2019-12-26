from rest_framework.views import APIView
from diancan_server.libs.geetest import GeetestLib
from django.conf import settings
import random
from rest_framework.response import Response
from django_redis import get_redis_connection


from .serializers import UserModelSerializer
from rest_framework.generics import CreateAPIView
from .models import User


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


