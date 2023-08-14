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
        super(CommentCreateModelForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
        self.fields['text'].label = 'Add comment:'

    def clean_text(self):
        text = self.cleaned_data.get('text')
        self.add_error(None, 'Error')
        if text.isspace():
            messages.error(
                self.request,
                "This field can not string contains only spaces."
            )

        return text

    def clean(self):
        if 'comment_order' in self.request.POST and self.request.POST.get('comment_order') != '':
            try:
                order = Order.objects.get(id=self.request.POST.get('comment_order'))
                self.order_obj = order
            except Order.DoesNotExist:
                self.add_error(None, 'Error')
                messages.error(
                    self.request,
                    "Order does not exist."
                )
        else:
            messages.error(
                self.request,
                "Order field are empty."
            )
