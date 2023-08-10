from django.forms import ModelForm, forms
from crm_app.models import Company
from phonenumber_field.widgets import PhoneNumberPrefixWidget
import re


class CompanyUpdateForm(ModelForm):
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
        name = self.cleaned_data.get('name')

        if name is not None and re.match(r'^\d+$', name):
            raise forms.ValidationError('It can`t be only digits')
        elif name is None:
            raise forms.ValidationError('You have to name your company')

        return name
