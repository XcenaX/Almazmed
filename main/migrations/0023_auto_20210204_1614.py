# Generated by Django 3.0.4 on 2021-02-04 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_license_preview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='lisence',
            field=models.FileField(upload_to='lisences'),
        ),
        migrations.AlterField(
            model_name='license',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to='previews'),
        ),
    ]
