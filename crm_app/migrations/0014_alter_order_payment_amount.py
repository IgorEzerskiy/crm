# Generated by Django 4.2.3 on 2023-07-18 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0013_alter_client_email_alter_client_telephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_amount',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]
