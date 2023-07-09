from django.urls import path

from crm_app.views import OrderListView, UserLoginView, UserLogoutView, UserCreateView

urlpatterns = [
    path('board/', OrderListView.as_view(), name='board'),
    path('', OrderListView.as_view(), name='main'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('registration/', UserCreateView.as_view(), name='registration')
]
