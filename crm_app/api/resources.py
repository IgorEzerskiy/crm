from rest_framework.generics import ListAPIView, CreateAPIView

from crm_app.api.serializers import OrderReadSerializer, UserReadSerializer, OrderCreateSerializer, \
    ClientModelSerializer
from crm_app.models import Order, User, Client, Status


class OrderListAPIView(ListAPIView):
    serializer_class = OrderReadSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(manager__company=self.request.user.company)


class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all()

    def get_serializer_context(self):
        context = super(OrderCreateAPIView, self).get_serializer_context()
        context.update(
            {"request": self.request}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(manager__company=self.request.user.company)

    def perform_create(self, serializer):
        serializer.validated_data['status'] = Status.objects.first()
        super().perform_create(serializer=serializer)


class UserListAPIView(ListAPIView):
    serializer_class = UserReadSerializer
    queryset = User.objects.all()


class ClientCreateAPIView(CreateAPIView):
    serializer_class = ClientModelSerializer
    queryset = Client.objects.all()

    def perform_create(self, serializer):
        serializer.validated_data['service_company'] = self.request.user.company
        super().perform_create(serializer=serializer)
