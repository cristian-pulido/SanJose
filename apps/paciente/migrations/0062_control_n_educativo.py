# Generated by Django 2.0.4 on 2018-07-31 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0061_auto_20180728_0003'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='n_educativo',
            field=models.CharField(choices=[('Primaria', 'Primaria'), ('Bachillerato', 'Bachillerato'), ('Técnico', 'Técnico'), ('Profesional', 'Profesional')], max_length=20, null=True),
        ),
    ]
