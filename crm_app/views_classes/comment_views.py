from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect
from django.views.generic import CreateView

from crm_app.forms_classes.comment_forms import CommentCreateModelForm
from crm_app.models import Order, Comment
from django.contrib import messages


class CommentCreateView(LoginRequiredMixin, CreateView):
    success_url = '/'
    login_url = '/login'
    queryset = Comment.objects.all()
    form_class = CommentCreateModelForm
    # template_name = 'board.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})

        return kwargs

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(author__company=self.request.user.company)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.order = form.order_obj
        comment.author = self.request.user
        comment.save()

        messages.success(
            self.request,
            "The comment was added successfully."
        )

        return super().form_valid(form=form)
