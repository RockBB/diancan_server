from django.urls import path, re_path
from . import views
urlpatterns = [
    path(r"foods/", views.CartAPIView.as_view()),

]