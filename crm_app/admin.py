from django.contrib import admin
from crm_app.models import Status, User, Client, Comment, Company, Order

admin.site.register(Status)
admin.site.register(User)
admin.site.register(Client)
admin.site.register(Comment)
admin.site.register(Company)
admin.site.register(Order)
