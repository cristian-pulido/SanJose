# Generated by Django 2.0.4 on 2018-04-30 03:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fileupload', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apatologicos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('HTA', 'HTA'), ('Diabetes', 'Diabetes'), ('IAM', 'IAM'), ('Hipotiroidismo', 'Hipotiroidismo'), ('Dislipidemia', 'Dislipidemia'), ('Otro', 'Otro')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sujeto_numero', models.CharField(max_length=20, null=True, unique=True)),
                ('fecha_de_registro', models.DateField(null=True)),
                ('cc', models.PositiveIntegerField(null=True, unique=True)),
                ('nombres', models.CharField(max_length=70, null=True)),
                ('apellidos', models.CharField(max_length=70, null=True)),
                ('edad', models.PositiveIntegerField(null=True)),
                ('sexo', models.CharField(choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer')], max_length=9, null=True)),
                ('HC', models.PositiveIntegerField(null=True, unique=True)),
                ('cama_numero', models.PositiveIntegerField(null=True)),
                ('fecha_evento_principal', models.DateField(null=True)),
                ('hora_evento_principal', models.TimeField(blank=True, default=datetime.time(0, 0), null=True)),
                ('fecha_ingreso', models.DateField(null=True)),
                ('hora_ingreso', models.TimeField(blank=True, default=datetime.time(0, 0), null=True)),
                ('G_diagnostico', models.CharField(choices=[('TCE', 'TCE'), ('Hipoxia/Anoxia', 'Hipoxia/Anoxia'), ('ACV', 'ACV')], max_length=20, null=True)),
                ('D_especificos', models.TextField(blank=True, null=True)),
                ('ci', models.CharField(choices=[('ci1', 'Paciente con episodio de parada cadíaca con reanimación exitosa'), ('ci2', 'Paciente con Dx de lesión cerebral aguda de origen traumático o evento cerebrovascular')], default='ci1', max_length=128, null=True)),
                ('ci3', models.NullBooleanField(verbose_name='Puntaje en escala Glasgow igual o menor a 8 después del evento inicial')),
                ('ci4', models.NullBooleanField(verbose_name='Paciente transportable a un resonador')),
                ('ce1', models.NullBooleanField(verbose_name='Diagnóstico de muerte cerebral en las primeras 48 horas del ingreso a UCI')),
                ('ce2', models.NullBooleanField(verbose_name='Destruccion masiva del parénquima cerebral no rescatable por neurocirugía')),
                ('ce3', models.NullBooleanField(verbose_name='Disfunción neurológica y/o neuropsiquiátrica previa')),
                ('ce4', models.NullBooleanField(verbose_name='Decisión de la familia de no participar en estudios de investigación')),
                ('estado', models.PositiveIntegerField(default=1, null=True)),
                ('inscrito', models.NullBooleanField(default=False)),
            ],
            options={
                'ordering': ('sujeto_numero',),
            },
        ),
        migrations.CreateModel(
            name='Dprevio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('Traumáticos', 'Traumáticos'), ('Degenerativos', 'Degenerativos'), ('Neoplásticos', 'Neoplásticos'), ('Vasculares', 'Vasculares'), ('Infecciosos', 'Infecciosos'), ('Metabólicos', 'Metabólicos'), ('Tx Neurodesarrollo', 'Tx Neurodesarrollo'), ('TX Psicótico', 'TX Psicótico'), ('Tx Afectivo', 'Tx Afectivo'), ('Deficit cognitivo', 'Deficit cognitivo'), ('Abuso de sustancias', 'Abuso de sustancias'), ('Otro', 'Otro')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ingreso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_form', models.DateField(null=True)),
                ('lugar_nacimiento', models.CharField(blank=True, max_length=80, null=True)),
                ('lugar_residencia', models.CharField(blank=True, max_length=80, null=True)),
                ('direccion', models.CharField(blank=True, max_length=100, null=True)),
                ('nombre_acompanante', models.CharField(blank=True, max_length=70, null=True)),
                ('tel1', models.PositiveIntegerField(blank=True, null=True)),
                ('tel2', models.PositiveIntegerField(blank=True, null=True)),
                ('peso', models.PositiveIntegerField(blank=True, null=True)),
                ('estatura', models.PositiveIntegerField(blank=True, null=True)),
                ('n_educativo', models.CharField(blank=True, choices=[('Primaria', 'Primaria'), ('Bachillerato', 'Bachillerato'), ('Técnico', 'Técnico'), ('Profesional', 'Profesional')], max_length=20, null=True)),
                ('lateralidad', models.CharField(blank=True, choices=[('Diestro', 'Diestro'), ('Zurdo', 'Zurdo'), ('Ambidiestro', 'Ambidiestro')], max_length=20, null=True)),
                ('conciencia', models.CharField(blank=True, choices=[('Coma', 'Coma'), ('SVSR', 'SVSR'), ('EMC', 'EMC')], max_length=20, null=True)),
                ('sedado', models.NullBooleanField(verbose_name='Sedado por neuroprotección')),
                ('a_patologicos_cual', models.CharField(max_length=50, null=True)),
                ('quirurgicos', models.CharField(blank=True, choices=[('craneotomia', 'Craneotomía'), ('otro', 'Otro')], max_length=128, null=True)),
                ('fecha_craneotomia', models.DateField(blank=True, null=True)),
                ('causa_quirurgicos', models.CharField(blank=True, max_length=100, null=True)),
                ('a_toxico_alergenicos', models.CharField(blank=True, max_length=180, null=True)),
                ('a_farmaco1', models.CharField(blank=True, max_length=180, null=True)),
                ('a_farmaco1_dosis', models.CharField(blank=True, max_length=30, null=True)),
                ('a_farmaco2', models.CharField(blank=True, max_length=180, null=True)),
                ('a_farmaco2_dosis', models.CharField(blank=True, max_length=30, null=True)),
                ('a_familiares', models.CharField(blank=True, max_length=180, null=True)),
                ('firma_consentimiento', models.BooleanField(default=True)),
                ('firma_causa', models.CharField(blank=True, max_length=50, null=True)),
                ('a_patologicos', models.ManyToManyField(blank=True, to='paciente.Apatologicos')),
                ('candidato', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='paciente.Candidato')),
            ],
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Radiologia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_procedimiento', models.DateField(null=True)),
                ('transportable', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('hora_inicio', models.TimeField(default=datetime.time(0, 0), null=True)),
                ('jefe_enfermeria', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('aux_enfermeria', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('medico_uci', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('anestesiologo', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('terapeuta_respiratorio', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('vmi', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('vasopresor', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('ionotropico', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('ur_pulsoximetro', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('ur_pulsoximetro_sv', models.CharField(blank=True, max_length=50, null=True)),
                ('ur_frecuencia_cardiaca', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('ur_frecuencia_cardiaca_sv', models.CharField(blank=True, max_length=50, null=True)),
                ('ur_frecuencia_respiratoria', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('ur_frecuencia_respiratoria_sv', models.CharField(blank=True, max_length=50, null=True)),
                ('ur_visoscopio', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('ur_visoscopio_sv', models.CharField(blank=True, max_length=50, null=True)),
                ('ur_tension', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('ur_tension_sv', models.CharField(blank=True, max_length=50, null=True)),
                ('pic', models.CharField(blank=True, max_length=25, null=True)),
                ('ppc', models.CharField(blank=True, max_length=25, null=True)),
                ('medicamentos_emergencia', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('me_cual', models.CharField(blank=True, max_length=25, null=True)),
                ('me_dosis', models.CharField(blank=True, max_length=25, null=True)),
                ('sedacion', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('sedacion_dt', models.CharField(blank=True, max_length=25, null=True)),
                ('sedacion_sv', models.CharField(blank=True, max_length=25, null=True)),
                ('analgesia', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('analgesia_dt', models.CharField(blank=True, max_length=25, null=True)),
                ('analgesia_sv', models.CharField(blank=True, max_length=25, null=True)),
                ('relajacion', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('relajacion_dt', models.CharField(blank=True, max_length=25, null=True)),
                ('relajacion_sv', models.CharField(blank=True, max_length=25, null=True)),
                ('otra_medicacion', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('otra_medicacion_dt', models.CharField(blank=True, max_length=25, null=True)),
                ('otra_medicacion_cual', models.CharField(blank=True, max_length=25, null=True)),
                ('ru_pulsoximetro', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('ru_pulsoximetro_sv', models.CharField(blank=True, max_length=50, null=True)),
                ('ru_frecuencia_cardiaca', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('ru_frecuencia_cardiaca_sv', models.CharField(blank=True, max_length=50, null=True)),
                ('ru_frecuencia_respiratoria', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('ru_frecuencia_respiratoria_sv', models.CharField(blank=True, max_length=50, null=True)),
                ('ru_visoscopio', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('ru_visoscopio_sv', models.CharField(blank=True, max_length=50, null=True)),
                ('ru_tension', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('ru_tension_sv', models.CharField(blank=True, max_length=50, null=True)),
                ('tiempo_sesonacia', models.CharField(max_length=50, null=True)),
                ('hora_llegada', models.TimeField(blank=True, default=datetime.time(0, 0), null=True)),
                ('complicaciones', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], max_length=12, null=True)),
                ('complicaciones_cuales', models.CharField(blank=True, max_length=150, null=True)),
                ('candidato', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='paciente.Candidato')),
            ],
        ),
        migrations.CreateModel(
            name='Uci',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechauci', models.DateField(null=True)),
                ('horauci', models.TimeField(default=datetime.time(0, 0), null=True)),
                ('apertura_ocular', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], max_length=5, null=True)),
                ('respuesta_motora', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], max_length=5, null=True)),
                ('respuesta_verbal', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], max_length=5, null=True)),
                ('glasgowtotal', models.CharField(default=0, max_length=5, null=True)),
                ('candidato', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='paciente.Candidato')),
            ],
        ),
        migrations.AddField(
            model_name='candidato',
            name='D_neuro_logico_psiquiatrico_previo',
            field=models.ManyToManyField(blank=True, to='paciente.Dprevio'),
        ),
        migrations.AddField(
            model_name='candidato',
            name='imagen',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fileupload.Picture'),
        ),
        migrations.AddField(
            model_name='candidato',
            name='medico_responsable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='paciente.Medico'),
        ),
    ]
