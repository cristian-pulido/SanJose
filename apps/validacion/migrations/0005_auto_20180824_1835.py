# Generated by Django 2.0.4 on 2018-08-24 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('validacion', '0004_auto_20180824_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tagsdicom',
            name='key_tag',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='tagsdicom',
            name='name_tag',
            field=models.CharField(max_length=200),
        ),
    ]
