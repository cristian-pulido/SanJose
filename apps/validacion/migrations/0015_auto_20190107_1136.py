# Generated by Django 2.0.4 on 2019-01-07 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('validacion', '0014_auto_20181031_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pipeline',
            name='etapa',
        ),
        migrations.RemoveField(
            model_name='task',
            name='pathout',
        ),
        migrations.AddField(
            model_name='pipeline',
            name='pathout',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
