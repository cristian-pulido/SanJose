# Generated by Django 2.0.4 on 2018-07-28 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0057_auto_20180726_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='seguimiento',
            name='imgobservacion',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='uci',
            name='dx_egreso',
            field=models.CharField(blank=True, default='', max_length=230, null=True),
        ),
    ]
