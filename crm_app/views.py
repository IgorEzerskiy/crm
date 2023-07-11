from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from crm_app.forms import UserLoginForm, UserCreateForm, ClientModelForm, CompanyForm
from crm_app.models import Order, Client, Company, User


# Create your views here.


class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'board.html'
    queryset = Order.objects.all()
    login_url = 'login/'


# Auth


class UserLoginView(LoginView):
    template_name = 'login.html'
    next_page = '/'
    form_class = UserLoginForm


class UserLogoutView(LoginRequiredMixin, LogoutView):
    http_method_names = ['post']
    next_page = '/'


class UserCreateView(CreateView):
    # API Done
    template_name = 'registration.html'
    form_class = UserCreateForm
    success_url = '/login'

    def form_valid(self, form):
        user = form.save(commit=False)
        company = Company.objects.filter(
            name=self.request.POST.get('company')
        )
        if company.exists():
            user.company = company.first()
            user.is_active = False
            user.save()
        else:
            with transaction.atomic():
                company = Company.objects.create(
                    name=self.request.POST.get('company')
                )
                user.company = company
                user.is_company_admin = True
                user.save()
        return super().form_valid(
            form=form
        )


class ClientListView(ListView):
    template_name = 'clients.html'
    queryset = Client.objects.all()
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            service_company=self.request.user.company
        )


class UserListView(ListView):
    template_name = 'users.html'
    queryset = User.objects.all()
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            company=self.request.user.company
        )


class ClientCreateView(CreateView):
    template_name = 'new_client.html'
    form_class = ClientModelForm
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {"request": self.request}
        )
        return kwargs

    def form_valid(self, form):
        return HttpResponseRedirect(self.success_url)


class ClientUpdateView(UpdateView):
    form_class = ClientModelForm
    queryset = Client.objects.all()
    template_name = 'edit_client.html'
    success_url = '/clients'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {"request": self.request}
        )
        return kwargs


class CompanyUpdateView(UpdateView):
    form_class = CompanyForm
    queryset = Company.objects.all()
    template_name = 'edit_company.html'
    success_url = '/'


class UserDetailView(DetailView):
    queryset = User.objects.all()
    template_name = 'profile.html'


class OrderCreateView(CreateView):
    pass
