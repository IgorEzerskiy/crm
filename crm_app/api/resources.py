from rest_framework.generics import ListAPIView

from crm_app.api.serializers import OrderReadSerializer, UserReadSerializer
from crm_app.models import Order, User


class OrderListAPIView(ListAPIView):
    serializer_class = OrderReadSerializer
    queryset = Order.objects.all()


class UserListAPIView(ListAPIView):
    serializer_class = UserReadSerializer
    queryset = User.objects.all()
