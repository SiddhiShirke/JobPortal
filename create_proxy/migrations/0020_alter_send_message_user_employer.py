# Generated by Django 3.2.9 on 2022-03-29 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('create_proxy', '0019_auto_20220329_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='send_message',
            name='user_employer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='create_proxy.employermore'),
        ),
    ]