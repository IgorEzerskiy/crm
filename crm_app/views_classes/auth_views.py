from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import CreateView

from crm_app.forms_classes.user_forms import UserLoginForm, UserCreateForm
from crm_app.models import Company
from django.contrib import messages


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
                messages.error(
                    self.request,
                    'Company does not exist.')
                return HttpResponseRedirect('/registration')
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
                messages.error(
                    self.request,
                    'Company already exist.')
                return HttpResponseRedirect('/registration')

        return super().form_valid(form=form)
