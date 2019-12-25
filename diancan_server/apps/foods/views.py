from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from .models import FoodCategory, Food
from .serializers import FoodModelSerializer


class FoodCategoryAPIView(ListAPIView):
    """课程分类列表"""
    queryset = FoodCategory.objects.filter(is_delete=False, is_show=True).order_by("orders")
    serializer_class = FoodModelSerializer


from rest_framework.pagination import PageNumberPagination


class StandardPageNumberPagination(PageNumberPagination):
    """自定义分页器"""
    page_size_query_param = 'page_size'
    max_page_size = 10
    page_size = 3


from .serializers import FoodModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class FoodAPIView(ListAPIView):
    """食物列表信息"""
    queryset = Food.objects.filter(is_delete=False, is_show=True).order_by("orders")
    serializer_class = FoodModelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ('food_category',)
    ordering_fields = ('id', 'name', 'price')
    pagination_class = StandardPageNumberPagination
