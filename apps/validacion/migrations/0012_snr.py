# Generated by Django 2.0.4 on 2018-09-29 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('validacion', '0011_auto_20180925_1329'),
    ]

    operations = [
        migrations.CreateModel(
            name='Snr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sujeto', models.CharField(blank=True, max_length=15, null=True)),
                ('structural', models.CharField(max_length=30, null=True)),
                ('funcional', models.CharField(max_length=30, null=True)),
                ('funcional_plot', models.CharField(blank=True, max_length=300, null=True)),
                ('tensor', models.CharField(max_length=30, null=True)),
                ('tensor_plot', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
    ]
