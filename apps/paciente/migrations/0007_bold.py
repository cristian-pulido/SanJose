# Generated by Django 2.0.4 on 2018-05-14 02:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0006_auto_20180513_2114'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bold',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaimg', models.DateField(null=True)),
                ('candidato', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='paciente.Candidato')),
            ],
        ),
    ]
