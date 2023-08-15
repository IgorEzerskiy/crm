from django.forms import ModelForm
from crm_app.models import Comment, Order

from django.contrib import messages


class CommentCreateModelForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        if 'kwargs' in kwargs:
            self.kwargs = kwargs.pop('kwargs')
        super(CommentCreateModelForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
        self.fields['text'].label = 'Add comment:'

    def clean(self):
        cleaned_data = super().clean()
        try:
            Order.objects.get(id=self.kwargs.get('pk'))
        except Order.DoesNotExist:
            self.add_error(None, 'Error')
            messages.error(
                self.request,
                "Order does not exist."
            )

        if cleaned_data.get('text') is None:
            self.add_error(None, 'Error')
            messages.error(
                self.request,
                "This field can not string contains only spaces."
            )
