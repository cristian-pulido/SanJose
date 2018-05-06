# Generated by Django 2.0.4 on 2018-05-05 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0009_auto_20180505_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='neurologia',
            name='alerta',
            field=models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='neurologia',
            name='total1',
            field=models.CharField(default=0, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='neurologia',
            name='verbal',
            field=models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='neurologia',
            name='visual',
            field=models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], max_length=100, null=True),
        ),
    ]
