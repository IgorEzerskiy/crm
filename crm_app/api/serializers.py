from rest_framework import serializers
from crm_app.models import Order, Company, User, Status, Client, Comment


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ClientReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name']


class StatusReadSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ['id', 'name']


class OrderReadSerializer(serializers.ModelSerializer):
    manager = UserReadSerializer()
    client = ClientReadSerializer()
    status = StatusReadSerilizer()

    class Meta:
        model = Order
        fields = [
            'id',
            'title',
            'description',
            'client',
            'manager',
            'start_date',
            'due_date',
            'status',
            'payment_amount',
        ]
