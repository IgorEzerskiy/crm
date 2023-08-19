from rest_framework.generics import ListAPIView, CreateAPIView

from crm_app.api.serializers import OrderReadSerializer, UserReadSerializer, OrderCreateSerializer, \
    ClientModelSerializer
from crm_app.models import Order, User, Client


class OrderListAPIView(ListAPIView):
    serializer_class = OrderReadSerializer
    queryset = Order.objects.all()


class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all()


class UserListAPIView(ListAPIView):
    serializer_class = UserReadSerializer
    queryset = User.objects.all()


class ClientCreateAPIView(CreateAPIView):
    serializer_class = ClientModelSerializer
    queryset = Client.objects.all()

    def perform_create(self, serializer):
        serializer.validated_data['service_company'] = self.request.user.company
        super().perform_create(serializer=serializer)
