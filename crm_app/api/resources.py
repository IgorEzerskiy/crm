import os

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response

from crm_app.api.permissions import IsCompanyAdminOrPermissionDenied, IsAuthenticatedOrPermissionDeny

from crm_app.api.serializers import UserModelSerializer, OrderModelSerializer, \
    ClientModelSerializer, CommentReadSerializer, CompanyModelSerializer, StatusReadSerializer, \
    ClientDeleteSerializer, RegisterSerializer
from crm_app.models import Order, User, Client, Status, Comment, Company


# Orders classes


class OrderListAPIView(ListAPIView):
    serializer_class = OrderModelSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(manager__company=self.request.user.company)


class OrderDetailAPIView(RetrieveAPIView):
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
    serializer_class = UserModelSerializer
    queryset = User.objects.all()


# Client classes


class ClientCreateAPIView(CreateAPIView):
    serializer_class = ClientModelSerializer
    queryset = Client.objects.all()

    def perform_create(self, serializer):
        serializer.validated_data['service_company'] = self.request.user.company
        super().perform_create(serializer=serializer)


class ClientListAPIView(ListAPIView):
    serializer_class = ClientModelSerializer
    queryset = Client.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(service_company=self.request.user.company)

        return queryset


class ClientUpdateAPIView(UpdateAPIView):
    serializer_class = ClientModelSerializer
    queryset = Client.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(service_company=self.request.user.company)

        return queryset


class ClientDestroyAPIView(DestroyAPIView):
    serializer_class = ClientDeleteSerializer
    queryset = Client.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(service_company=self.request.user.company)

        return queryset

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #
    #     serializer = self.get_serializer()
    #
    #     client_first_last_name = serializer.data['first_name_and_last_name'].split('-')
    #
    #
    #     # self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# Comments classes


class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentReadSerializer

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        super().perform_create(serializer=serializer)


# Companies classes
class CompanyUpdateAPIView(UpdateAPIView):
    serializer_class = CompanyModelSerializer
    queryset = Company.objects.all()


# Profile classes
class ProfileAPIView(RetrieveAPIView):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.kwargs['pk'] == self.request.user.id:
            raise ValidationError('Invalid profile pk')

        return queryset.filter(company=self.request.user.company)


class ProfileUpdateAPIView(UpdateAPIView):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()

    def perform_update(self, serializer):
        current_image = None if self.request.user.image.name == '' else self.request.user.image
        new_image = serializer.validated_data.get('image')

        if new_image is None:
            super().perform_update(serializer=serializer)
        else:
            if current_image:
                os.remove(current_image.path)
        super().perform_update(serializer=serializer)


# Status classes

class StatusReadAPIView(ListAPIView):
    serializer_class = StatusReadSerializer
    queryset = Status.objects.all()


class UserCreateAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

