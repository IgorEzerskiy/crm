from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.forms import ModelChoiceField
from crm_app.forms_classes.order_forms import OrderModelForm
from crm_app.forms_classes.comment_forms import CommentCreateModelForm
from crm_app.models import Order, Client, User, Status
from django.contrib import messages
# from crm_app.views_classes.permissions import AdminPassedMixin

# API Done


class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'board.html'
    queryset = Order.objects.all()
    login_url = 'login/'
    extra_context = {'comment_form': CommentCreateModelForm}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()

        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            client__service_company=self.request.user.company,
        )

        if 'orders_filter' in self.request.GET:
            if self.request.GET.get('orders_filter') == 'all':
                """"""
            if self.request.GET.get('orders_filter') == 'active':
                queryset = queryset.filter(
                    is_active_order=True
                )
            if self.request.GET.get('orders_filter') == 'hidden':
                queryset = queryset.filter(
                    is_active_order=False
                )

        if 'orders_filter_managers' in self.request.GET:
            if self.request.GET.get('orders_filter_managers') != 'all':
                try:
                    manager = User.objects.get(
                        id=self.request.GET.get('orders_filter_managers')
                    )
                    queryset = queryset.filter(
                        manager=manager
                    )
                except User.DoesNotExist:
                    messages.error(
                        self.request,
                        f'Manager does not exist.'
                    )

        if 'orders_filter_clients' in self.request.GET:
            if self.request.GET.get('orders_filter_clients') != 'all':
                try:
                    client = Client.objects.get(
                        id=self.request.GET.get('orders_filter_clients')
                    )
                    queryset = queryset.filter(
                        client=client
                    )
                except Client.DoesNotExist:
                    messages.error(
                        self.request,
                        f'Client does not exist.'
                    )

        return queryset


class OrderCreateView(LoginRequiredMixin, CreateView):
    template_name = 'new_order.html'
    form_class = OrderModelForm
    success_url = '/'
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        clients = self.request.user.company.clients

        managers = self.request.user.company.user

        context['form'].fields['client'] = ModelChoiceField(queryset=clients)

        context['form'].fields['manager'] = ModelChoiceField(queryset=managers)

        context['form'].fields['client'].widget.attrs.update({'class': 'form-control'})

        context['form'].fields['manager'].widget.attrs.update({'class': 'form-control'})

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "request": self.request,
            "view": 'create_view'
        })

        return kwargs

    def form_valid(self, form):
        order = form.save(commit=False)
        status = Status.objects.first()
        order.status = status
        order.save()

        messages.success(
            self.request,
            "Order was create successfully."
        )

        return super().form_valid(form=form)


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'update_order.html'
    queryset = Order.objects.all()
    form_class = OrderModelForm
    success_url = '/'
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        managers = self.request.user.company.user
        context['form'].fields['manager'] = ModelChoiceField(queryset=managers)
        context['form'].fields['manager'].widget.attrs.update({'class': 'form-control'})

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "request": self.request,
            "view": 'update_view'
        })

        return kwargs

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(manager__company=self.request.user.company)

    def form_valid(self, form):
        messages.success(
            self.request,
            "Order was update successfully."
        )

        return super().form_valid(form=form)
