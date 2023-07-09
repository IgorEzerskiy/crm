from django.shortcuts import render
from django.views.generic import ListView

from crm_app.models import Order


# Create your views here.


class OrderListView(ListView):
    template_name = 'board.html'
    queryset = Order.objects.all()
