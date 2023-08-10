from django.forms import ModelForm
from crm_app.models import Comment


class CommentCreateModelForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super(CommentCreateModelForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
        self.fields['text'].label = 'Add comment:'
