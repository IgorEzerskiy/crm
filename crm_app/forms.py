from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import CharField, ModelForm, forms, DateField, SelectDateWidget, \
    DateInput  # WHY form was imported????
from crm_app.models import User, Company, Client, Order, Comment
from phonenumber_field.widgets import PhoneNumberPrefixWidget
import re


class CustomDateInput(DateInput):
    input_type = 'date'


class UserCreateForm(UserCreationForm):
    company = CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', )

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['company'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username)
        if user.exists():
            if not user.first().is_active:
                raise forms.ValidationError(
                    'Wait until the administrator of your company confirms the request to add you.'
                )
        else:
            raise forms.ValidationError(
                'Invalid username.'
            )

        return username


class ClientModelForm(ModelForm):
    class Meta:
        model = Client
        fields = ('first_name',
                  'last_name',
                  'telephone',
                  'email',
                  'telegram',
                  'slack',
                  )
        widgets = {
            'telephone': PhoneNumberPrefixWidget(country_attrs={
                'style': 'width:150px; margin-bottom:15px',
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


class CompanyUpdateForm(ModelForm):
    class Meta:
        model = Company
        fields = ('name',
                  'telephone',
                  'email',
                  )
        widgets = {
            'telephone': PhoneNumberPrefixWidget(country_attrs={
                'style': 'width:150px, margin-left:15px',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(CompanyUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['telephone'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name is not None and re.match(r'^\d+$', name):
            raise forms.ValidationError('It can`t be only digits')
        elif name is None:
            raise forms.ValidationError('You have to name your company')

        return name


class OrderCreateForm(ModelForm):
    start_date = DateField(widget=CustomDateInput())
    due_date = DateField(widget=CustomDateInput())

    class Meta:
        model = Order
        fields = ('title',
                  'description',
                  'client',
                  'manager',
                  'start_date',
                  'due_date',
                  'payment_amount',
                  )

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['client'].widget.attrs.update({'class': 'form-control'})
        self.fields['manager'].widget.attrs.update({'class': 'form-control'})
        self.fields['start_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['due_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['payment_amount'].widget.attrs.update({'class': 'form-control', 'min': 0})

    def clean_payment_amount(self):
        payment_amount = self.cleaned_data.get('payment_amount')
        if payment_amount < 0:
            raise forms.ValidationError('Payment amount field must have value more then 0.')

        return payment_amount

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        due_date = cleaned_data.get('due_date')

        if start_date and due_date:
            if start_date > due_date:
                self.add_error('start_date', 'Start date should be earlier than due date.')
                self.add_error('due_date', 'Due date should be later than start date.')

        return cleaned_data
