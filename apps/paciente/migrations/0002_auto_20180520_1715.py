# Generated by Django 2.0.4 on 2018-05-20 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidato',
            name='archivo',
            field=models.FileField(null=True, upload_to='Documentos'),
        ),
    ]
