from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import ListView, UpdateView, DetailView, DeleteView
from crm_app.forms_classes.user_forms import PasswordChangeForm, UserInfoUpdateForm
from crm_app.models import User
from django.contrib import messages
import os
from crm_app.views_classes.permissions import AdminPassedMixin

# API Done


class UserListView(AdminPassedMixin, LoginRequiredMixin, ListView):
    template_name = 'users.html'
    queryset = User.objects.all()
    paginate_by = 10
    login_url = '/login'

    def get_queryset(self):
        queryset = super().get_queryset().filter(company=self.request.user.company)

        if self.request.GET.get('users_filter') == 'all':
            return queryset.annotate(
                order_num=Count('order')
            )
        if self.request.GET.get('users_filter') == 'admins':
            return queryset.filter(
                is_company_admin=True
            ).annotate(
                order_num=Count('order')
            )
        if self.request.GET.get('users_filter') == 'managers':
            return queryset.exclude(
                is_company_admin=True
            ).annotate(
                order_num=Count('order')
            )

        return queryset.annotate(
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
        user = self.object
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


class UserConnectionApproveView(AdminPassedMixin, LoginRequiredMixin, UpdateView):
    login_url = '/login'
    success_url = '/user-connection-requests'
    queryset = User.objects.all()
    fields = ()

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(company=self.request.user.company)

    def form_valid(self, form):
        if not self.object.is_active:
            self.object.is_active = True
            messages.success(
                self.request,
                'User added to your company successfully.'
            )
        else:
            messages.error(
                self.request,
                'User is already added to your company.'
            )

        return super().form_valid(form=form)


class UserConnectionDeleteView(AdminPassedMixin, LoginRequiredMixin, DeleteView):
    login_url = '/login'
    success_url = '/user-connection-requests'
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(company=self.request.user.company)

    def form_valid(self, form):
        if self.object:
            messages.success(
                self.request,
                "The user's request was rejected successfully."
            )

        return super().form_valid(form=form)

# API Done


class UserDetailView(LoginRequiredMixin, DetailView):
    queryset = User.objects.all()
    template_name = 'profile.html'
    extra_context = {'form': PasswordChangeForm}

# API Done


class ProfileInfoUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'update_profile.html'
    queryset = User.objects.all()
    form_class = UserInfoUpdateForm
    success_url = '/'
    login_url = 'login/'

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
            return super().form_valid(form=form)
        else:
            if current_img:
                os.remove(current_img.path)
            obj.save()

        return super().form_valid(form=form)


class PasswordUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    model = User
    form_class = PasswordChangeForm
    success_url = '/'
    login_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})

        return kwargs


class UsersUpdateView(AdminPassedMixin, LoginRequiredMixin, UpdateView):
    template_name = 'users_update.html'
    queryset = User.objects.all()
    form_class = UserInfoUpdateForm
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "request": self.request,
            "user_id": self.kwargs['pk']
        })

        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        current_user = self.object
        new_img = form.cleaned_data.get('image')
        current_img = None if current_user.image.name == '' else current_user.image

        if new_img == current_img:
            messages.success(
                self.request,
                "The user information has been successfully updated."
            )

            return super().form_valid(form=form)
        else:
            if current_img:
                os.remove(current_img.path)
            obj.save()

        messages.success(
            self.request,
            "The user information has been successfully updated."
        )

        return super().form_valid(form=form)
