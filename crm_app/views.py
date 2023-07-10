from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView

from crm_app.forms import UserLoginForm, UserCreateForm, ClientCreateForm, CompanyForm
from crm_app.models import Order, Client, Company


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


class ClientUpdateView(UpdateView):
    form_class = ClientCreateForm
    queryset = Client.objects.all()
    template_name = 'edit_client.html'
    success_url = '/clients'


class CompanyUpdateView(UpdateView):
    form_class = CompanyForm
    queryset = Company.objects.all()
    template_name = 'edit_company.html'
    success_url = '/'


class OrderCreateView(CreateView):
    pass
