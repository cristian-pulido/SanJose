# Generated by Django 2.0.4 on 2018-06-19 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0013_auto_20180618_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seguimiento',
            name='fechaseguimiento',
            field=models.DateField(null=True),
        ),
    ]
