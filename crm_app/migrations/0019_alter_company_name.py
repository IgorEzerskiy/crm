# Generated by Django 4.2.3 on 2023-08-07 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0018_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]