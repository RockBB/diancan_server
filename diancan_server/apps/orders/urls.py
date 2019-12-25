from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.OrderAPIView.as_view()),
    re_path("(?P<pk>\d+)/", views.OrderDetailAPIView.as_view()),
]
