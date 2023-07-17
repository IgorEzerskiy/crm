from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.forms import ModelChoiceField
from crm_app.forms import UserLoginForm, UserCreateForm, ClientModelForm, CompanyUpdateForm, OrderCreateForm
from crm_app.models import Order, Client, Company, User, Status, Comment


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
        context['orders'] = Order.objects.filter(
            client__service_company=self.request.user.company
        )
        context['comments'] = Comment.objects.filter(
            author__company=self.request.user.company
        )

        return context


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


class ClientListView(LoginRequiredMixin, ListView):
    template_name = 'clients.html'
    queryset = Client.objects.all()
    paginate_by = 10
    login_url = '/login'

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(
            service_company=self.request.user.company
        )


class UserListView(AdminPassedMixin, LoginRequiredMixin, ListView):
    template_name = 'users.html'
    queryset = User.objects.all()
    paginate_by = 10
    login_url = '/login'

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(
            company=self.request.user.company
        )


class UserConnectionRequestsListView(AdminPassedMixin, LoginRequiredMixin, ListView):
    template_name = 'users_connection_requests.html'
    queryset = User.objects.all()
    paginate_by = 10
    login_url = '/login'

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(
            company=self.request.user.company, is_active=False
        )

    def post(self, request, *args, **kwargs):
        approved_id = self.request.POST.get('approve_user_id')
        cancel_id = self.request.POST.get('cancel_user_id')

        if approved_id:
            try:
                user = User.objects.get(id=approved_id)
                user.is_active = True
                user.save()
            except User.DoesNotExist:
                # TODO: Add message
                pass

        if cancel_id:
            try:
                user = User.objects.get(id=cancel_id)
                user.delete()
            except User.DoesNotExist:
                # TODO: Add message
                pass

        return HttpResponseRedirect('/users-connections-requests')


class ClientCreateView(LoginRequiredMixin, CreateView):
    template_name = 'new_client.html'
    form_class = ClientModelForm
    success_url = '/'
    login_url = '/login'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {"request": self.request}
        )

        return kwargs

    def form_valid(self, form):
        client = form.save(commit=False)
        client.service_company = self.request.user.company

        return super().form_valid(
            form=form
        )


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ClientModelForm
    queryset = Client.objects.all()
    template_name = 'edit_client.html'
    success_url = '/clients'
    login_url = '/login'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {"request": self.request}
        )

        return kwargs


class CompanyUpdateView(AdminPassedMixin, LoginRequiredMixin, UpdateView):
    form_class = CompanyUpdateForm
    queryset = Company.objects.all()
    template_name = 'edit_company.html'
    success_url = '/'
    login_url = '/login'


class UserDetailView(LoginRequiredMixin, DetailView):
    queryset = User.objects.all()
    template_name = 'profile.html'


class OrderCreateView(LoginRequiredMixin, CreateView):
    template_name = 'new_order.html'
    form_class = OrderCreateForm
    success_url = '/'
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_form = context['form']

        clients = Client.objects.filter(
            service_company=self.request.user.company
        )
        managers = User.objects.filter(
            company=self.request.user.company
        )

        order_form.fields['client'] = ModelChoiceField(queryset=clients)
        order_form.fields['client'].widget.attrs.update({'class': 'form-control'})
        order_form.fields['manager'] = ModelChoiceField(queryset=managers)
        order_form.fields['manager'].widget.attrs.update({'class': 'form-control'})
        context['new_order'] = order_form

        return context

    def form_valid(self, form):
        order = form.save(commit=False)
        status = Status.objects.first()
        order.status = status
        order.save()

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
            order = Order.objects.get(id=comment_order)
            if len(comment_text) < 450:
                # TODO: Add message
                pass
            if comment_text and comment_order:
                Comment.objects.create(
                    text=comment_text,
                    order=order,
                    author=self.request.user)
            else:
                # TODO: Add message
                pass
        except Order.DoesNotExist:
            # TODO: Add message
            pass

        return HttpResponseRedirect(self.success_url)
