# Generated by Django 3.2.9 on 2022-02-12 15:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create_proxy', '0004_alter_applied_jobs_applied_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applied_jobs',
            name='applied_date',
            field=models.DateField(default=datetime.date(2022, 2, 12)),
        ),
    ]