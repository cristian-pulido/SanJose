# Generated by Django 2.0.4 on 2019-03-25 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procesamiento', '0002_results'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='results',
            options={'permissions': (('can_ver_resultados', 'puede ver resultados'),)},
        ),
        migrations.AddField(
            model_name='results',
            name='tipo',
            field=models.CharField(choices=[('Imagen', 'Imagen'), ('Grafica', 'Grafica'), ('Texto', 'Texto'), ('Archivo nii', 'Archivo nii')], max_length=40, null=True),
        ),
    ]
