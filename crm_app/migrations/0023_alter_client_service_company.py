# Generated by Django 4.2.3 on 2023-08-08 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0022_alter_client_service_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='service_company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='clients', to='crm_app.company'),
        ),
    ]
