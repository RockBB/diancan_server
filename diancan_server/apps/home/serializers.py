from rest_framework.serializers import ModelSerializer
from .models import BannerInfo
class BannerInfoSerializer(ModelSerializer):
    class Meta:
        model=BannerInfo
        fields = ("image","link")


from rest_framework.serializers import ModelSerializer
from .models import NavInfo
class NavInfoSerializer(ModelSerializer):
    class Meta:
        model=NavInfo
        fields = ("name","link")