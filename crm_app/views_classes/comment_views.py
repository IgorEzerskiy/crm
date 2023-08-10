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

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(author__company=self.request.user.company)

    def form_valid(self, form):
        comment = form.save(commit=False)

        if 'comment_order' in self.request.POST and self.request.POST.get('comment_order') != '':
            try:
                order = Order.objects.get(id=self.request.POST.get('comment_order'))
                comment.order = order
            except Order.DoesNotExist:
                messages.error(
                    self.request,
                    "Order does not exist."
                )

                return HttpResponseRedirect(self.success_url)
        else:
            messages.error(
                self.request,
                "Order field are empty."
            )
            return HttpResponseRedirect(self.success_url)
        comment.author = self.request.user

        messages.success(
            self.request,
            "The comment was added successfully."
        )

        return super().form_valid(form=form)
