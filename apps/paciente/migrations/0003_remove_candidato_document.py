# Generated by Django 2.0.4 on 2018-05-12 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0002_candidato_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidato',
            name='document',
        ),
    ]
