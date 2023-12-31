# Generated by Django 3.2.9 on 2022-02-12 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create_proxy', '0008_employermore_company_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='total_working_hours',
            field=models.CharField(default='12hrs', max_length=200),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='job_type',
            field=models.CharField(choices=[('1-months-internship', '1-Months Internship'), ('2-months-internship', '2-Months Internship'), ('3-months-internship', '3-Months Internship'), ('4-months-internship', '4-Months Internship'), ('5-months-internship', '5-Months Internship'), ('6-months-internship', '6-Months Internship'), ('7-months-internship', '7-Months Internship'), ('8-months-internship', '8-Months Internship'), ('9-months-internship', '9-Months Internship'), ('10-months-internship', '10-Months Internship'), ('11-months-internship', '11-Months Internship'), ('12-months-internship', '12-Months Internship'), ('full-time', 'Full-Time'), ('part-time', 'Part-Time')], default='full-time', max_length=50),
        ),
    ]
