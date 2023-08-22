from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView

from crm_app.api.serializers import UserReadSerializer, OrderModelSerializer, \
    ClientModelSerializer, CommentReadSerializer
from crm_app.models import Order, User, Client, Status, Comment

# Orders classes


class OrderListAPIView(ListAPIView):
    serializer_class = OrderModelSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(manager__company=self.request.user.company)


class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderModelSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(manager__company=self.request.user.company)

    def perform_create(self, serializer):
        serializer.validated_data['status'] = Status.objects.first()
        super().perform_create(serializer=serializer)


class OrderUpdateAPIView(UpdateAPIView):
    serializer_class = OrderModelSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(manager__company=self.request.user.company)

# Users classes


class UserListAPIView(ListAPIView):
    serializer_class = UserReadSerializer
    queryset = User.objects.all()

# Client classes


class ClientCreateAPIView(CreateAPIView):
    serializer_class = ClientModelSerializer
    queryset = Client.objects.all()

    def perform_create(self, serializer):
        serializer.validated_data['service_company'] = self.request.user.company
        super().perform_create(serializer=serializer)

# Comments classes


class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentReadSerializer
    queryset = Comment

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(order__manager__company=self.request.user.company)

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        super().perform_create(serializer=serializer)

# Companies classes
