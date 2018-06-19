# Generated by Django 2.0.4 on 2018-06-19 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0011_auto_20180618_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seguimiento',
            name='candidato',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='paciente.Candidato', unique_for_date='fechaseguimiento'),
        ),
        migrations.AlterField(
            model_name='seguimiento',
            name='fechaseguimiento',
            field=models.DateField(null=True),
        ),
    ]
