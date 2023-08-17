from rest_framework.generics import ListAPIView

from crm_app.api.serializers import OrderReadSerializer
from crm_app.models import Order


class OrderListAPIView(ListAPIView):
    serializer_class = OrderReadSerializer
    queryset = Order.objects.all()