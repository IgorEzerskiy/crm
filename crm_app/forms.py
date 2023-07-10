from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import CharField, ModelForm, forms
from django.db import transaction
from crm_app.models import User, Company, Client
from phonenumber_field.widgets import PhoneNumberPrefixWidget


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


class ClientModelForm(ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'telephone', 'email', 'telegram', 'slack', ]
        widgets = {
            'telephone': PhoneNumberPrefixWidget(country_attrs={
                'style': 'width:100px',
            }),
        }

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ClientModelForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['telephone'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['telegram'].widget.attrs.update({'class': 'form-control'})
        self.fields['slack'].widget.attrs.update({'class': 'form-control'})
        # self.fields['service_company'].widget.attrs.update({'class': 'form-control'})



    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError('Only letter')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError('Only letter')
        return last_name

    def clean_telegram(self):
        telegram = self.cleaned_data.get('telegram')
        if telegram is not None and not telegram.startswith('@'):
            raise forms.ValidationError('It should starts with "@"')
        return telegram

    def save(self, commit=True):
        self.instance = Client.objects.create(
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            slack=self.cleaned_data.get('slack'),
            telephone=self.cleaned_data.get('telephone'),
            telegram=self.cleaned_data.get('telegram'),
            email=self.cleaned_data.get('email'),
            service_company=self.request.user.company
        )



class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'telephone', 'email')
        widgets = {
            'telephone': PhoneNumberPrefixWidget(country_attrs={
                'style': 'width:100px',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['telephone'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
