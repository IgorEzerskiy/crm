from rest_framework.generics import ListAPIView, CreateAPIView

from crm_app.api.serializers import OrderReadSerializer, UserReadSerializer, OrderCreateSerializer
from crm_app.models import Order, User


class OrderListAPIView(ListAPIView):
    serializer_class = OrderReadSerializer
    queryset = Order.objects.all()


class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all()


class UserListAPIView(ListAPIView):
    serializer_class = UserReadSerializer
    queryset = User.objects.all()
