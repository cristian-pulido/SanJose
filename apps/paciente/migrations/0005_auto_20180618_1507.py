# Generated by Django 2.0.4 on 2018-06-18 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0004_auto_20180612_1400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidato',
            name='fecha_ingreso',
        ),
        migrations.RemoveField(
            model_name='candidato',
            name='hora_ingreso',
        ),
        migrations.AddField(
            model_name='candidato',
            name='fecha_hora_ingreso',
            field=models.DateTimeField(null=True),
        ),
    ]
