from django.urls import path

from crm_app.views import OrderListView

urlpatterns = [
    path('board/', OrderListView.as_view(), name='board'),
    path('', OrderListView.as_view(), name='main'),
]
