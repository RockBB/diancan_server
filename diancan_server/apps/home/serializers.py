from rest_framework.serializers import ModelSerializer
from .models import BannerInfo
class BannerInfoSerializer(ModelSerializer):
    """轮播图序列化器"""
    class Meta:
        model=BannerInfo
        fields = ("image","link")


from rest_framework.serializers import ModelSerializer
from .models import NavInfo
class NavInfoSerializer(ModelSerializer):
    """导航序列化器"""
    class Meta:
        model=NavInfo
        fields = ("name","link")