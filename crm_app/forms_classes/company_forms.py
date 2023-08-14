from django.forms import ModelForm, forms, EmailField
from crm_app.models import Company
from phonenumber_field.widgets import PhoneNumberPrefixWidget
import re

from crm_app.validators import email_validator


class CompanyUpdateForm(ModelForm):
    email = EmailField(
        validators=[email_validator],
        required=False
    )

    class Meta:
        model = Company
        fields = (
            'name',
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
        name_row = self.cleaned_data.get('name')
        name = name_row.strip()

        if name is not None and re.match(r'^\d+$', name):
            raise forms.ValidationError('It can`t be only digits')
        elif re.search(r'\s{2,}', name):
            raise forms.ValidationError('Two or more spaces in a row. Please enter name correctly.')
        elif name is None:
            raise forms.ValidationError('You have to name your company')

        return name
