# Generated by Django 3.1.7 on 2021-05-13 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0044_auto_20210513_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='gos_services',
            field=models.ManyToManyField(blank=True, null=True, to='main.GovermentService'),
        ),
    ]
