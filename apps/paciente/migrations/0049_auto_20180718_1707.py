# Generated by Django 2.0.4 on 2018-07-18 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0048_auto_20180716_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidato',
            name='ci',
            field=models.CharField(blank=True, choices=[('ci1', 'Paciente con episodio de parada cardíaca con reanimación exitosa'), ('ci2', 'Paciente con Dx de lesión cerebral aguda de origen traumático'), ('cie', 'Paciente con Dx de lesión cerebral aguda por evento cerebrovascular')], default='ci1', max_length=128, null=True),
        ),
    ]
