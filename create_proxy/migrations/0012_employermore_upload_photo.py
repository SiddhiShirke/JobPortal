# Generated by Django 3.2.9 on 2022-02-13 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create_proxy', '0011_alter_candidatemore_upload_cv'),
    ]

    operations = [
        migrations.AddField(
            model_name='employermore',
            name='upload_photo',
            field=models.ImageField(blank=True, upload_to='profile_image'),
        ),
    ]
