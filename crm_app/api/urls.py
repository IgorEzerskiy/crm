from rest_framework.authtoken.views import ObtainAuthToken
from django.urls import path

from crm_app.api.resources import OrderListAPIView, UserListAPIView, OrderCreateAPIView

urlpatterns = [
    path('login/', ObtainAuthToken.as_view()),
    path('orders/', OrderListAPIView.as_view()),
    path('users/', UserListAPIView.as_view()),
    path('order-create/', OrderCreateAPIView.as_view())
]
