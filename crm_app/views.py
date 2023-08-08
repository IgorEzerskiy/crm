from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.forms import ModelChoiceField

from crm_app.forms import UserLoginForm, UserCreateForm, ClientModelForm, CompanyUpdateForm, OrderCreateForm, \
    OrderUpdateForm, PasswordChangeForm, UserInfoUpdateForm
from crm_app.models import Order, Client, Company, User, Status, Comment
from django.contrib import messages
import os


# Create your views here.
class AdminPassedMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_company_admin


class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'board.html'
    queryset = Order.objects.all()
    login_url = 'login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['comments'] = Comment.objects.filter(
            author__company=self.request.user.company
        )
        context['managers'] = User.objects.filter(
            company=self.request.user.company
        )
        context['clients'] = Client.objects.filter(
            service_company=self.request.user.company
        )

        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            client__service_company=self.request.user.company,
        )

        if 'orders_filter' in self.request.GET:
            if self.request.GET.get('orders_filter') == 'all':
                queryset = queryset.filter(
                    client__service_company=self.request.user.company
                )
            if self.request.GET.get('orders_filter') == 'active':
                queryset = queryset.filter(
                    client__service_company=self.request.user.company,
                    is_active_order=True
                )
            if self.request.GET.get('orders_filter') == 'hidden':
                queryset = queryset.filter(
                    client__service_company=self.request.user.company,
                    is_active_order=False
                )

        if 'orders_filter_managers' in self.request.GET:
            if self.request.GET.get('orders_filter_managers') != 'all':
                try:
                    manager = User.objects.get(
                        id=self.request.GET.get('orders_filter_managers')
                    )
                    queryset = queryset.filter(
                        client__service_company=self.request.user.company,
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


# Auth


class UserLoginView(LoginView):
    template_name = 'login.html'
    next_page = '/'
    form_class = UserLoginForm


class UserLogoutView(LoginRequiredMixin, LogoutView):
    http_method_names = ['post']
    next_page = '/'


class UserCreateView(CreateView):
    template_name = 'registration.html'
    form_class = UserCreateForm
    success_url = '/login'

    def form_valid(self, form):
        new_user_obj = form.save(commit=False)

        if not self.request.POST.get('create_company'):
            try:
                company = Company.objects.get(name=self.request.POST.get('company'))
                new_user_obj.company = company
                new_user_obj.is_active = False
                new_user_obj.save()
                messages.success(
                    self.request,
                    f'HI, {new_user_obj.username}. You have been added to the company {company.name}. '
                    f'Wait for company administrator confirmation.'
                )
            except Company.DoesNotExist:
                form.add_error('company', 'Company does not exist.')
                return self.form_invalid(form=form)
        else:
            if not Company.objects.get(name=self.request.POST.get('company')):
                username = new_user_obj.username
                with transaction.atomic():
                    company = Company.objects.create(name=self.request.POST.get('company'))
                    new_user_obj.company = company
                    new_user_obj.is_company_admin = True
                    new_user_obj.save()
                messages.success(
                    self.request,
                    f'HI, {username}. You created a new company called: {company.name}.'
                )
            else:
                form.add_error('company', 'Company already exist.')
                return self.form_invalid(form=form)

        return super().form_valid(form=form)


class ClientListView(LoginRequiredMixin, ListView):
    template_name = 'clients.html'
    queryset = Client.objects.all()
    paginate_by = 10
    login_url = '/login'

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.GET.get('clients_filter') == 'all':
            return queryset.filter(
                service_company=self.request.user.company
            ).annotate(
                order_num=Count('order')
            )
        if self.request.GET.get('clients_filter') == 'active':
            return queryset.filter(
                service_company=self.request.user.company,
                is_active_client=True
            ).annotate(
                order_num=Count('order')
            )
        if self.request.GET.get('clients_filter') == 'inactive':
            return queryset.filter(
                service_company=self.request.user.company,
                is_active_client=False
            ).annotate(
                order_num=Count('order')
            )
        return queryset.filter(
            service_company=self.request.user.company
        ).annotate(
                order_num=Count('order')
            )


class UserListView(AdminPassedMixin, LoginRequiredMixin, ListView):
    template_name = 'users.html'
    queryset = User.objects.all()
    paginate_by = 10
    login_url = '/login'

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.GET.get('users_filter') == 'all':
            return queryset.filter(
                company=self.request.user.company
            ).annotate(
                order_num=Count('order')
            )
        if self.request.GET.get('users_filter') == 'admins':
            return queryset.filter(
                company=self.request.user.company,
                is_company_admin=True
            ).annotate(
                order_num=Count('order')
            )
        if self.request.GET.get('users_filter') == 'managers':
            return queryset.filter(
                company=self.request.user.company,

            ).exclude(
                is_company_admin=True
            ).annotate(
                order_num=Count('order')
            )

        return queryset.filter(
            company=self.request.user.company
        ).annotate(
            order_num=Count('order')
        )


class UserDeleteView(AdminPassedMixin, LoginRequiredMixin, DeleteView):
    login_url = 'login/'
    success_url = '/users'
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(company=self.request.user.company)

    def form_valid(self, form):
        user = self.get_object()
        username = self.request.POST.get('user_name')

        current_img = None if user.image.name == '' else user.image

        if username == user.username:
            if current_img:
                os.remove(current_img.path)
            messages.success(
                self.request,
                "Manager was delete successfully."
            )
        else:
            messages.error(
                self.request,
                "Error deleting manager. The manager's username entered is not correct."
            )

        return super().form_valid(form=form)


class UserConnectionRequestsListView(AdminPassedMixin, LoginRequiredMixin, ListView):
    template_name = 'users_connection_requests.html'
    queryset = User.objects.all()
    paginate_by = 10
    login_url = '/login'

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(
            company=self.request.user.company,
            is_active=False
        )

    def post(self, request, *args, **kwargs):
        approved_id = self.request.POST.get('approve_user_id')
        cancel_id = self.request.POST.get('cancel_user_id')

        if approved_id:
            try:
                user = User.objects.get(
                    id=approved_id
                )
                user.is_active = True
                user.save()
                messages.success(
                    self.request,
                    'User added to your company successfully.'
                )
            except User.DoesNotExist:
                messages.error(
                    self.request,
                    f'User does not exist.'
                )

        if cancel_id:
            try:
                user = User.objects.get(
                    id=cancel_id
                )
                user.delete()
                messages.success(
                    self.request,
                    "The user's request was rejected successfully."
                )
            except User.DoesNotExist:
                messages.error(
                    self.request,
                    f'User does not exist.'
                )

        return HttpResponseRedirect('/user-connection-requests')


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


class CompanyUpdateView(AdminPassedMixin, LoginRequiredMixin, UpdateView):
    form_class = CompanyUpdateForm
    queryset = Company.objects.all()
    template_name = 'edit_company.html'
    success_url = '/'
    login_url = '/login'

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(name=self.request.user.company.name)

    def get_success_url(self):
        url = super().get_success_url()

        return url + f'profile/{self.request.user.id}'

    def form_valid(self, form):
        messages.success(
            self.request,
            "Company was update successfully."
        )

        return super().form_valid(form=form)


class UserDetailView(LoginRequiredMixin, DetailView):
    queryset = User.objects.all()
    template_name = 'profile.html'
    extra_context = {'form': PasswordChangeForm}


class OrderCreateView(LoginRequiredMixin, CreateView):
    template_name = 'new_order.html'
    form_class = OrderCreateForm
    success_url = '/'
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order_form = context['form']

        clients = Client.objects.filter(service_company=self.request.user.company)

        managers = User.objects.filter(company=self.request.user.company)

        order_form.fields['client'] = ModelChoiceField(queryset=clients)

        order_form.fields['manager'] = ModelChoiceField(queryset=managers)

        order_form.fields['client'].widget.attrs.update({'class': 'form-control'})

        order_form.fields['manager'].widget.attrs.update({'class': 'form-control'})

        context['new_order'] = order_form

        return context

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

#  ---------------------------------------------------------------------------------------


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'update_order.html'
    queryset = Order.objects.all()
    form_class = OrderUpdateForm
    success_url = '/'
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        managers = User.objects.filter(
            company=self.request.user.company
        )
        context['form'].fields['manager'] = ModelChoiceField(
            queryset=managers
        )
        context['form'].fields['manager'].widget.attrs.update(
            {'class': 'form-control'}
        )

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(
            manager__company=self.request.user.company
        )

    def form_valid(self, form):
        messages.success(
            self.request,
            "Order was update successfully."
        )

        return super().form_valid(
            form=form
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    success_url = '/'
    login_url = '/login'

    def post(self, request, *args, **kwargs):
        comment_text = self.request.POST.get('comment_text')
        comment_order = self.request.POST.get('comment_order')

        try:
            order = Order.objects.get(
                id=comment_order
            )
            if len(comment_text) > 450:
                messages.error(
                    self.request,
                    "Your comment contains more than 450 characters."
                )
                return HttpResponseRedirect(self.success_url)
            if comment_text and comment_order:
                Comment.objects.create(
                    text=comment_text,
                    order=order,
                    author=self.request.user
                )
            else:
                messages.error(
                    self.request,
                    "Error creating comment."
                )
                return HttpResponseRedirect(self.success_url)
        except Order.DoesNotExist:
            messages.error(
                self.request,
                "Order does not exist."
            )

        return HttpResponseRedirect(self.success_url)


class ClientDeleteView(AdminPassedMixin, LoginRequiredMixin, DeleteView):
    login_url = 'login/'
    success_url = '/clients'
    queryset = Client.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(
            service_company=self.request.user.company
        )

    def form_valid(self, form):
        client = self.get_object()
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


class ProfileInfoUpdateView(UpdateView):
    template_name = 'update_profile.html'
    queryset = User.objects.all()
    form_class = UserInfoUpdateForm
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def get_success_url(self):
        url = super().get_success_url()
        return url + f'profile/{self.request.user.id}'

    def form_valid(self, form):
        obj = form.save(commit=False)
        new_img = form.cleaned_data.get('image')
        current_img = None if self.request.user.image.name == '' else self.request.user.image

        if new_img == current_img:
            return super().form_valid(
                form=form
            )
        else:
            if current_img:
                os.remove(current_img.path)
            obj.save()
        return super().form_valid(
            form=form
        )


class PasswordUpdateView(UpdateView):
    template_name = 'profile.html'
    model = User
    form_class = PasswordChangeForm
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs


class ClientRecoveryUpdateView(UpdateView):
    model = Client
    success_url = '/clients'
    fields = ()

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

        return super().form_valid(
            form=form
        )


class UsersUpdateView(UpdateView):
    template_name = 'users_update.html'
    queryset = User.objects.all()
    form_class = UserInfoUpdateForm
    success_url = '/users/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "request": self.request,
            "user_id": self.kwargs['pk']
        })
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        current_user = User.objects.get(id=self.kwargs['pk'])
        new_img = form.cleaned_data.get('image')
        current_img = None if current_user.image.name == '' else current_user.image

        if new_img == current_img:
            return super().form_valid(
                form=form
            )
        else:
            if current_img:
                os.remove(current_img.path)
            obj.save()
        return super().form_valid(
            form=form
        )
