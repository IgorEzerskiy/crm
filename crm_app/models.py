from django.contrib.auth.models import AbstractUser
from django.db import models
from phone_field import PhoneField


class Company(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    telephone = PhoneField(null=False, blank=False, unique=True)
    email = models.EmailField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=45)
    client_company_name = models.CharField(max_length=100)
    telephone = PhoneField(null=False, blank=False, unique=True)
    email = models.EmailField(null=False, blank=False, unique=True)
    telegram = models.CharField(max_length=60)
    slack = models.CharField(max_length=60)
    service_company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.first_name + '_' + self.last_name + '_' + self.client_company_name


class Status(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class User(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='user')

    def __str__(self):
        return self.username


class Order(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=550)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, related_name='order')
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='order')
    start_date = models.DateField()
    due_date = models.DateField()
    payment_amount = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)


class Comment(models.Model):
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=450)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'Comment for order: {self.order.title[0:15]} by author {self.author.first_name}_{self.author.last_name}'
