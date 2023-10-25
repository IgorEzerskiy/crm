from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import UpdateView

from crm_app.forms_classes.company_forms import CompanyUpdateForm

from crm_app.models import Company
from django.contrib import messages

from crm_app.views_classes.permissions import AdminPassedMixin

# API Done


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
