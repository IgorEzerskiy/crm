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


class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'title',
            'description',
            'client',
            'manager',
            'status',
            'start_date',
            'due_date',
            'payment_amount',
        ]
        read_only_fields = ['id']

    def get_fields(self):
        fields = super().get_fields()
        allowed_methods = ['GET']
        if self.context['request'].stream.method in allowed_methods:
            fields['status'] = StatusReadSerializer()
            fields['manager'] = UserReadSerializer()
            fields['client'] = ClientModelSerializer()
            fields['comments'] = CommentReadSerializer(many=True)
        return fields

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
