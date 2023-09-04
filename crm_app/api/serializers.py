import re

from rest_framework import serializers
from crm_app.models import Order, Company, User, Status, Client, Comment


class CommentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
            'created_at',
            'updated_at',
            'order',
            'author'
        ]
        read_only_fields = [
            'id',
            'updated_at',
            'created_at',
            'author'
        ]

    def validate_order(self, value):
        if value.manager.company != self.context['request'].user.company:
            raise serializers.ValidationError('Invalid order ID. Order not in your company.')
        return value


class CompanyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id',
            'name',
            'telephone',
            'email'
        ]
        extra_kwargs = {
            'email': {'write_only': True},
        }
        read_only_fields = ['id']

        def validate_name(self, value):
            name = value.strip()
            if name is not None and re.match(r'^\d+$', name):
                raise serializers.ValidationError('It can`t be only digits')
            elif re.search(r'\s{2,}', name):
                raise serializers.ValidationError('Two or more spaces in a row. Please enter name correctly.')
            elif name is None:
                raise serializers.ValidationError('You have to name your company')

            return name


class UserModelSerializer(serializers.ModelSerializer):
    company = CompanyModelSerializer()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'company',
            'is_company_admin',
            'email',
            'image'
        ]
        read_only_fields = ['id', 'company', 'is_company_admin']

    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('Only letter')

        return value

    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('Only letter')

        return value


class ClientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id',
            'first_name',
            'last_name',
            'telephone',
            'telegram',
            'email'
        ]
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
        fields = [
            'id',
            'name'
        ]


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
        if self.context['request'].method in allowed_methods:
            fields['status'] = StatusReadSerializer()
            fields['manager'] = UserModelSerializer()
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
