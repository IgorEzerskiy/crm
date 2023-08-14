from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Company(models.Model):
    name = models.CharField(
                            max_length=100,
                            unique=True
                            )
    telephone = PhoneNumberField()
    email = models.EmailField()

    def __str__(self):
        return self.name


class Client(models.Model):
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=45)
    is_active_client = models.BooleanField(default=True)
    telephone = PhoneNumberField()
    email = models.EmailField(
                              null=True,
                              blank=True
                              )
    telegram = models.CharField(
                                max_length=60,
                                null=True,
                                blank=True
                               )
    service_company = models.ForeignKey(
                                        Company,
                                        on_delete=models.DO_NOTHING,
                                        related_name='clients'
                                        )

    def __str__(self):
        return self.first_name + '_' + self.last_name + '_' + self.service_company.name


class Status(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class User(AbstractUser):
    company = models.ForeignKey(
                                Company,
                                on_delete=models.CASCADE,
                                related_name='user'
                                )
    is_company_admin = models.BooleanField(default=False)
    image = models.ImageField(
                              upload_to='crm_app/static/profile_images/',
                              max_length=100,
                              null=True
                              )

    def __str__(self):
        return self.username


class Order(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=550)
    client = models.ForeignKey(
                               Client,
                               on_delete=models.DO_NOTHING,
                               related_name='order',
                               )
    manager = models.ForeignKey(
                                User,
                                on_delete=models.DO_NOTHING,
                                related_name='order'
                                )
    start_date = models.DateField()
    due_date = models.DateField()
    payment_amount = models.DecimalField(
                                         max_digits=15,
                                         decimal_places=2
                                         )
    status = models.ForeignKey(
                               Status,
                               on_delete=models.DO_NOTHING
                               )
    is_active_order = models.BooleanField(default=True)


class Comment(models.Model):
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=450)
    order = models.ForeignKey(
                              Order,
                              on_delete=models.CASCADE,
                              related_name='comments')
    author = models.ForeignKey(
                               User,
                               on_delete=models.DO_NOTHING,
                               related_name='comments'
                               )

    def __str__(self):
        return f'Comment for order: {self.order.title[0:15]} by author {self.author.first_name}_{self.author.last_name}'
