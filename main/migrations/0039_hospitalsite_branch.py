# Generated by Django 2.2.19 on 2021-03-12 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_doctor_has_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitalsite',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Branch'),
        ),
    ]
