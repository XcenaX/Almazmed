# Generated by Django 4.2.1 on 2023-10-16 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_city_uslugi_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='lisence',
            field=models.FileField(max_length=20000, upload_to='lisences'),
        ),
    ]
