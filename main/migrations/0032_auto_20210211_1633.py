# Generated by Django 3.1.6 on 2021-02-11 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_service_servicetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='code',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='service',
            name='count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
