# Generated by Django 4.2.3 on 2023-07-09 18:29

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0004_alter_user_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='telephone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True),
        ),
    ]
