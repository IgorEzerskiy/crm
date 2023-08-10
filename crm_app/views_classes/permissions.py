from django.contrib.auth.mixins import UserPassesTestMixin


class AdminPassedMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_company_admin
