from rest_framework import serializers
from crm_app.models import Order, Company, User, Status, Client, Comment
from crm_app.validators import email_validator, telegram_username_validator


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


class ClientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'telephone', 'telegram', 'email']
        read_only_fields = ['id']
        extra_kwargs = {
            'telephone': {'write_only': True},
            'telegram': {'write_only': True},
            'email': {'write_only': True}
        }
        
    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('Only letter')

        return value

    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('Only letter')

        return value


class StatusReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']


class OrderReadSerializer(serializers.ModelSerializer):
    manager = UserReadSerializer(read_only=True)
    client = ClientModelSerializer(read_only=True)
    status = StatusReadSerializer(read_only=True)
    comments = CommentReadSerializer(read_only=True, many=True)

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


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'title',
            'description',
            'client',
            'manager',
            'start_date',
            'due_date',
            'payment_amount',
        ]

    def validate_payment_amount(self, value):
        if value < 0:
            raise serializers.ValidationError('Payment amount field must have value more then 0.')
        return value

    def validate(self, attrs):
        if attrs['start_date'] > attrs['due_date']:
            raise serializers.ValidationError(
                {
                    'start_date': 'Start date should be earlier than due date.',
                    'due_date': 'Due date should be later than start date.'
                }
            )

        if attrs['manager'].company != self.context['request'].user.company:
            raise serializers.ValidationError({'manager': 'Manager not in your company.'})

        if attrs['client'].service_company != self.context['request'].user.company:
            raise serializers.ValidationError({'client': 'Client not in your company.'})

        return attrs
