# Generated by Django 3.1.7 on 2021-05-13 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_directorblog'),
    ]

    operations = [
        migrations.CreateModel(
            name='GovermentFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='gov_services_files')),
            ],
        ),
        migrations.CreateModel(
            name='GovermentService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='')),
                ('files', models.ManyToManyField(blank=True, null=True, to='main.GovermentFile')),
            ],
        ),
    ]
