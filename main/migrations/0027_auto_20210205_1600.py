# Generated by Django 3.1.6 on 2021-02-05 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_remove_microdistrict_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='number',
        ),
        migrations.AddField(
            model_name='house',
            name='name',
            field=models.TextField(default=''),
        ),
    ]
