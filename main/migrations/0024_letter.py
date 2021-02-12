# Generated by Django 3.1.6 on 2021-02-04 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20210204_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.TextField(default='')),
                ('text', models.TextField(default='')),
                ('letter', models.FileField(blank=True, null=True, upload_to='letters')),
            ],
        ),
    ]
