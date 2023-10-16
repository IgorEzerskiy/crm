from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from crm_app.forms_classes.client_forms import ClientModelForm
from crm_app.models import Order, Client
from django.contrib import messages

from crm_app.views_classes.permissions import AdminPassedMixin

# API Done


class ClientListView(LoginRequiredMixin, ListView):
    template_name = 'clients.html'
    queryset = Client.objects.all()
    paginate_by = 10
    login_url = '/login'

    def get_queryset(self):
        queryset = super().get_queryset().filter(service_company=self.request.user.company)

        if self.request.GET.get('clients_filter') == 'all':
            return queryset.annotate(
                order_num=Count('order')
            )
        if self.request.GET.get('clients_filter') == 'active':
            return queryset.filter(
                is_active_client=True
            ).annotate(
                order_num=Count('order')
            )
        if self.request.GET.get('clients_filter') == 'inactive':
            return queryset.filter(
                is_active_client=False
            ).annotate(
                order_num=Count('order')
            )
        return queryset.annotate(
            order_num=Count('order')
        )

# API Done


class ClientCreateView(LoginRequiredMixin, CreateView):
    template_name = 'new_client.html'
    form_class = ClientModelForm
    success_url = '/'
    login_url = '/login'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})

        return kwargs

    def form_valid(self, form):
        client = form.save(commit=False)
        client.service_company = self.request.user.company

        messages.success(
            self.request,
            "Client was create successfully."
        )

        return super().form_valid(form=form)

# API Done


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ClientModelForm
    queryset = Client.objects.all()
    template_name = 'edit_client.html'
    success_url = '/clients'
    login_url = '/login'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})

        return kwargs

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(service_company=self.request.user.company)

    def form_valid(self, form):
        messages.success(
            self.request,
            "Client was update successfully."
        )

        return super().form_valid(form=form)


class ClientDeleteView(AdminPassedMixin, LoginRequiredMixin, DeleteView):
    login_url = 'login/'
    success_url = '/clients'
    queryset = Client.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(service_company=self.request.user.company)

    def form_valid(self, form):
        client = self.object
        orders = Order.objects.filter(
            client__id=client.id,
            manager__company=self.request.user.company
        )
        client_first_last_name = self.request.POST.get('client_f_l_name').split('-')

        if client_first_last_name[0] == client.first_name \
                and client_first_last_name[1] == client.last_name:
            if 'real_deletion' in self.request.POST and self.request.POST.get('real_deletion'):
                messages.success(
                    self.request,
                    "Client was delete successfully FOREVER."
                )
                return super().form_valid(form=form)
            else:
                with transaction.atomic():
                    for order in orders:
                        order.is_active_order = False
                        order.save()
                    client.is_active_client = False
                    client.save()
                messages.success(
                    self.request,
                    "Client was delete successfully."
                )
        else:
            messages.error(
                self.request,
                "Error deleting client. The user's first and last name entered is not correct."
            )

        return HttpResponseRedirect(self.get_success_url())


class ClientRecoveryUpdateView(AdminPassedMixin, LoginRequiredMixin, UpdateView):
    model = Client
    success_url = '/clients'
    fields = ()
    login_url = 'login/'

    def form_valid(self, form):
        orders = Order.objects.filter(
            client__id=self.object.id,
            manager__company=self.request.user.company
        )

        with transaction.atomic():
            for order in orders:
                order.is_active_order = True
                order.save()
            self.object.is_active_client = True
            self.object.save()

        return super().form_valid(form=form)
