# Generated by Django 2.0.4 on 2018-06-10 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0002_auto_20180609_1703'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidato',
            options={},
        ),
        migrations.AlterField(
            model_name='candidato',
            name='sujeto_numero',
            field=models.PositiveIntegerField(null=True, unique=True),
        ),
    ]
