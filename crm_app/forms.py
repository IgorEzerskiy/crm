from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import CharField
from django.db import transaction
from crm_app.models import User, Company


class UserCreateForm(UserCreationForm):

    company = CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username']

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        self.company_status = False
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['company'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def clean_company(self):
        company = self.cleaned_data.get('company')
        if Company.objects.filter(name=company).exists():
            self.company_status = True
        return company

    def save(self, commit=True):
        if self.company_status:
            company = Company.objects.get(name=self.cleaned_data.get('company'))
            User.objects.create_user(
                username=self.cleaned_data.get('username'),
                password=self.cleaned_data.get('password'),
                company=company
            )
        else:
            with transaction.atomic():
                Company.objects.create(name=self.cleaned_data.get('company'))
                User.objects.create_superuser(
                    username=self.cleaned_data.get('username'),
                    password=self.cleaned_data.get('password'),
                    company=Company.objects.get(name=self.cleaned_data.get('company'))
                )


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
