# Generated by Django 3.1.6 on 2021-02-10 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_directionofactivity_branch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='is_working',
        ),
        migrations.AddField(
            model_name='doctor',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
