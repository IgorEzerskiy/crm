from django.forms import ModelForm, forms, DateField, NumberInput
from crm_app.models import Order


class OrderModelForm(ModelForm):
    start_date = DateField(widget=NumberInput(attrs={'type': 'date'}))
    due_date = DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'title',
            'description',
            'client',
            'manager',
            'start_date',
            'due_date',
            'status',
            'payment_amount',
        )

    def __init__(self, *args, **kwargs):
        if 'view' in kwargs:
            self.view_status = kwargs.pop('view')
        if 'request' in kwargs:
            kwargs.pop('request')

        super(OrderModelForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['client'].widget.attrs.update({'class': 'form-control'})
        self.fields['manager'].widget.attrs.update({'class': 'form-control'})
        self.fields['start_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['due_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['payment_amount'].widget.attrs.update({'class': 'form-control', 'min': 0})

        if self.view_status == 'create_view':
            self.fields.pop('status')
        if self.view_status == 'update_view':
            self.fields.pop('client')

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
