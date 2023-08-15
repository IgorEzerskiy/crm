from django.forms import ModelForm, forms, EmailField, CharField
from crm_app.models import Client
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from crm_app.validators import email_validator, telegram_username_validator


class ClientModelForm(ModelForm):
    email = EmailField(
        validators=[email_validator],
        required=False
    )

    telegram = CharField(
        validators=[telegram_username_validator],
        required=False
    )

    class Meta:
        model = Client
        fields = (
            'first_name',
            'last_name',
            'telephone',
            'email',
            'telegram',
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
