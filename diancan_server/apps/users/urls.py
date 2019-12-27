from django.urls.conf import path, re_path
from rest_framework_jwt.views import obtain_jwt_token
from . import views
urlpatterns = [
    path(r'login/', obtain_jwt_token),
    path(r'register/', views.UserAPIView.as_view()),
    path(r'money/', views.UserMoneyAPIView.as_view()),
    re_path(r'(?P<pk>\d+)/orders/', views.UserOrderAPIView.as_view()),

]