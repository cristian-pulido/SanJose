# Generated by Django 2.0.4 on 2018-06-20 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0020_auto_20180619_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seguimiento',
            name='parada_tiempo',
            field=models.CharField(blank=True, default='', max_length=12, null=True),
        ),
    ]
