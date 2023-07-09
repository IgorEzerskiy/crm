from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import ListView, CreateView

from crm_app.forms import UserLoginForm, UserCreateForm, ClientCreateForm
from crm_app.models import Order, Client


# Create your views here.


class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'board.html'
    queryset = Order.objects.all()
    login_url = 'login/'


# Auth


class UserLoginView(LoginView):
    # API Done
    template_name = 'login.html'
    form_class = UserLoginForm
    next_page = '/'


class UserLogoutView(LoginRequiredMixin, LogoutView):
    http_method_names = ['post']
    next_page = '/'


class UserCreateView(CreateView):
    # API Done
    template_name = 'registration.html'
    form_class = UserCreateForm
    success_url = 'login/'


class ClientListView(ListView):
    template_name = 'clients.html'
    queryset = Client.objects.all()


class ClientCreateView(CreateView):
    template_name = 'new_client.html'
    form_class = ClientCreateForm
    success_url = '/'


class OrderCreateView(CreateView):
    pass
