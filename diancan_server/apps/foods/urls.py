from django.urls import path, re_path
from . import views
urlpatterns = [
    path(r"cate/", views.FoodCategoryAPIView.as_view()),
    path(r"list/", views.FoodAPIView.as_view()),

]





