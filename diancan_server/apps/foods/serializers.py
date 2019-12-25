from rest_framework import serializers
from .models import FoodCategory, Food
class FoodCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ("id","name")


class FoodModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        #fields = ("id","name","food_img","brief","pub_date","food_category","price")
        fields = ("__all__")

