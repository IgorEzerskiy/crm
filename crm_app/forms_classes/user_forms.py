import re

from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import CharField, ModelForm, forms, PasswordInput, EmailField, ImageField, FileInput, BooleanField
from crm_app.models import User
from crm_app.validators import email_validator


class UserCreateForm(UserCreationForm):
    company = CharField(max_length=100)
    first_name = CharField(
        required=True,
        max_length=150
    )
    last_name = CharField(
        required=True,
        max_length=150
    )
    create_company = BooleanField(
        required=False
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name'
        )

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['company'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['create_company'].widget.attrs.update({'class': 'form-check-input'})

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


class PasswordChangeForm(ModelForm):
    current_password = CharField(
        max_length=128,
        widget=PasswordInput()
    )
    confirm_password = CharField(
        max_length=128,
        widget=PasswordInput()
    )

    class Meta:
        model = User
        fields = ['password']

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')

        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['current_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['confirm_password'].widget.attrs.update({'class': 'form-control'})

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')

        if not self.request.user.check_password(current_password):
            self.add_error(None, "Error")
            messages.error(
                self.request,
                "Invalid current password"
            )

        return current_password

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if password is None or len(password) < 8 or len(password) > 20 or ' ' in password:
            self.add_error(None, "Error")
            messages.error(
                self.request,
                "Invalid new password"
            )

        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if confirm_password != password:
            self.add_error(None, "Error")
            messages.error(
                self.request,
                "Password unconfirmed"
            )

        return confirm_password

    def clean(self):
        cleaned_data = super().clean()
        password = make_password(cleaned_data.get('password'))
        cleaned_data['password'] = password


class UserInfoUpdateForm(ModelForm):
    email = EmailField(
        validators=[email_validator],
        required=False
    )
    image = ImageField(
        widget=FileInput(
            attrs={"id": "image_field",
                   "style": "width : 250px ; margin-top: 21px",
                   }
        ),
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'is_company_admin',
            'image'
        ]

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')

        if 'user_id' in kwargs:
            self.user_id = kwargs.pop('user_id')

        super(UserInfoUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})

        if hasattr(self, 'user_id'):
            self.fields.pop("username")

        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_company_admin'].widget.attrs.update({'class': 'form-check-input',
                                                             'id': 'flexCheckDefault'
                                                             })

        if not self.request.user.is_company_admin:
            self.fields.pop('is_company_admin')

    def clean_is_company_admin(self):
        is_company_admin_from_form = self.cleaned_data.get('is_company_admin')

        if not self.request.user.is_company_admin:
            raise forms.ValidationError('An ordinary manager cannot give anyone the status of a company administrator.')

        return is_company_admin_from_form

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if first_name and not first_name.isalpha():
            raise forms.ValidationError('Only letter')

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if last_name and not last_name.isalpha():
            raise forms.ValidationError('Only letter')

        return last_name

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username:
            raise forms.ValidationError(
                'Invalid username.'
            )

        return username
