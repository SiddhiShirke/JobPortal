# Generated by Django 3.2.9 on 2022-03-29 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('create_proxy', '0018_send_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='send_message',
            old_name='user2',
            new_name='user_candidate',
        ),
        migrations.RemoveField(
            model_name='send_message',
            name='user1',
        ),
        migrations.AddField(
            model_name='send_message',
            name='user_employer',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='create_proxy.user'),
            preserve_default=False,
        ),
    ]