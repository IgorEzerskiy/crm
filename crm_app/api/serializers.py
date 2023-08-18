from rest_framework import serializers
from crm_app.models import Order, Company, User, Status, Client, Comment


class CommentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'updated_at']


class CompanyReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'telephone']


class UserReadSerializer(serializers.ModelSerializer):
    company = CompanyReadSerializer()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'company',
            'is_company_admin'
        ]


class ClientReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name']


class StatusReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']


class OrderReadSerializer(serializers.ModelSerializer):
    manager = UserReadSerializer()
    client = ClientReadSerializer()
    status = StatusReadSerializer()
    comments = CommentReadSerializer(many=True)

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
            'comments'
        ]
