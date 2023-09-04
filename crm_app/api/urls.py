from rest_framework.authtoken.views import ObtainAuthToken
from django.urls import path

from crm_app.api.resources import OrderListAPIView, UserListAPIView, OrderCreateAPIView, ClientCreateAPIView, \
    OrderUpdateAPIView, CommentCreateAPIView, OrderDetailAPIView, ProfileAPIView, ProfileUpdateAPIView, \
    CompanyUpdateAPIView

urlpatterns = [
    path('login/', ObtainAuthToken.as_view()),
    path('orders/', OrderListAPIView.as_view()),
    path('order-detail-view/<int:pk>', OrderDetailAPIView.as_view()),
    path('users/', UserListAPIView.as_view()),
    path('order-create/', OrderCreateAPIView.as_view()),
    path('client-create/', ClientCreateAPIView.as_view()),
    path('order-update/<int:pk>', OrderUpdateAPIView.as_view()),
    path('comment-add/', CommentCreateAPIView.as_view()),
    path('profile/<int:pk>', ProfileAPIView.as_view()),
    path('profile-update/<int:pk>', ProfileUpdateAPIView.as_view()),
    path('company-update/<int:pk>', CompanyUpdateAPIView.as_view()),

]
