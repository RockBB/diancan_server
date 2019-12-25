from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from django.db.models import Q
from .models import BannerInfo
from .serializers import BannerInfoSerializer


class BannerInfoListAPIView(ListAPIView):
    """
    轮播图列表
    """
    # queryset = BannerInfo.objects.filter(Q(is_show=True) & Q(is_delete=False)).order_by("-orders")
    queryset = BannerInfo.objects.filter(is_show=True, is_delete=False).order_by("-orders")
    serializer_class = BannerInfoSerializer


from .models import NavInfo
from .serializers import NavInfoSerializer


class NavInfoAPIView(ListAPIView):
    """
    导航列表
    """
    queryset = NavInfo.objects.filter(Q(is_show=True) & Q(is_delete=False) & Q(opt=0)).order_by("orders")
    serializer_class = NavInfoSerializer


class FooterInfoAPIView(ListAPIView):
    """
    导航列表
    """
    queryset = NavInfo.objects.filter(Q(is_show=True) & Q(is_delete=False) & Q(opt=1)).order_by("orders")
    serializer_class = NavInfoSerializer
