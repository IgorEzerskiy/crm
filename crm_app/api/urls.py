from rest_framework.authtoken.views import ObtainAuthToken
from django.urls import path

urlpatterns = [
    path('login/', ObtainAuthToken.as_view()),
]