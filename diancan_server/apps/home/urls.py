from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r"banner/", views.BannerInfoListAPIView.as_view()),
    path(r"nav/", views.NavInfoAPIView.as_view()),
    path(r"footer/", views.FooterInfoAPIView.as_view()),
]
